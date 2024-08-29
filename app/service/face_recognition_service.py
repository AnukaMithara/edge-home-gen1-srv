import asyncio
import pickle
import numpy as np
from queue import Queue
import cv2
import threading
from fastapi.responses import StreamingResponse
import time

from deepface import DeepFace

from app.config.config import FACE_RECOGNITION_THRESHOLD
from app.config.logging_config import get_logger
from app.entity.device_logs import DeviceLogs
from app.entity.user_logs import UserLogs
from app.repository.device_logs_repository import DeviceLogsRepository
from app.repository.device_repository import DeviceRepository
from app.repository.user_face_data_repository import UserFaceDataRepository
from app.repository.user_logs_repository import UserLogsRepository
from app.repository.user_repository import UserRepository
from app.service.websocket_service import WebsocketService
from app.config.database_config import DatabaseConfig

logger = get_logger(class_name=__name__)

websocket_service = WebsocketService()

streaming_devices = {}


class FaceRecognitionService:

    @classmethod
    def start_capture(cls, device_id, target_device_id, cam_source):
        if device_id in streaming_devices:
            return f"Already capturing for device {device_id}"
        cam_source = int(cam_source) if cam_source.isdigit() else cam_source
        streaming_devices[device_id] = {'frame': None}
        thread = threading.Thread(target=cls.process_frames,
                                  args=(device_id, target_device_id, cam_source, DatabaseConfig.get_database_session()),
                                  daemon=True)
        streaming_devices[device_id]['thread'] = thread
        thread.start()
        return {"message": f"Started capturing for device {device_id}"}

    @classmethod
    def load_embeddings_from_db(cls, db):
        try:
            logger.info("Load embeddings from database")
            data = UserFaceDataRepository.get_verified_users(db)
            known_embeddings = [(user_face_data.user_id, np.array(pickle.loads(user_face_data.face_data))) for
                                user_face_data in data]
            logger.info("Embeddings loaded successfully")
            return known_embeddings
        except Exception as ex:
            logger.error(f"Load embeddings error: {str(ex)}")
            return []

    @classmethod
    def identify_face(cls, frame, known_embeddings):
        try:
            result = DeepFace.represent(img_path=frame, model_name="Facenet", enforce_detection=False)
            if not result:
                return None

            frame_embedding = np.array(result[0]["embedding"])

            for user_id, embedding in known_embeddings:
                if frame_embedding.shape != embedding.shape:
                    continue

                distance = np.linalg.norm(frame_embedding - embedding)
                print(f"Distance from user {user_id}: {distance} -- Threshold: {FACE_RECOGNITION_THRESHOLD}")
                if distance < FACE_RECOGNITION_THRESHOLD:
                    logger.info(f"User {user_id} identified")
                    return user_id
        except Exception as e:
            logger.error(f"Error in identifying face: {str(e)}")
            return None

    @classmethod
    def process_frames(cls, device_id, target_device_id, cam_source, db):
        known_embeddings = cls.load_embeddings_from_db(db)
        detected_user = None
        frame_queue = Queue(maxsize=10)

        def frame_processing_thread():
            nonlocal detected_user
            while detected_user is None:
                frame = frame_queue.get()
                if frame is None:
                    break

                rgb_frame = cv2.cvtColor(frame['small_frame'], cv2.COLOR_BGR2RGB)
                user_id = cls.identify_face(rgb_frame, known_embeddings)
                if user_id:
                    detected_user = user_id
                frame_queue.task_done()

                if detected_user:
                    asyncio.run(cls.handle_post_detection(user_id, target_device_id))

        processing_thread = threading.Thread(target=frame_processing_thread, daemon=True)
        processing_thread.start()

        # Retry mechanism
        max_retries = 5
        retry_delay = 5  # seconds
        attempt = 0
        cap = None

        while attempt < max_retries:
            cap = cv2.VideoCapture(cam_source, cv2.CAP_FFMPEG)
            # cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
            cap.set(cv2.CAP_PROP_FPS, 10)

            if not cap.isOpened():
                logger.error(f"Attempt {attempt + 1}: Could not open video stream from {cam_source}")
                attempt += 1
                time.sleep(retry_delay)
            else:
                break

        if cap is None or not cap.isOpened():
            logger.error(f"Failed to open video stream from {cam_source} after {max_retries} attempts")
            return

        frame_skip = 5
        frame_count = 0

        while device_id in streaming_devices:
            ret, frame = cap.read()
            if not ret:
                logger.error(f"Failed to read frame from {cam_source}. Exiting...")
                break

            frame_count += 1
            small_frame = cv2.resize(frame, (320, 240))

            if frame_count % frame_skip == 0 and not frame_queue.full():
                frame_queue.put({'small_frame': small_frame, 'original_frame': frame})

            if detected_user:
                user = UserRepository.get_user_by_id(detected_user, db)
                cv2.putText(frame, f"User {user.first_name} {user.last_name} identified", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Detecting...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            streaming_devices[device_id]['frame'] = frame

        cap.release()
        frame_queue.put(None)
        processing_thread.join()

    @classmethod
    async def handle_post_detection(cls, user_id, target_device_id):
        logger.info(f"User {user_id} identified")
        db = DatabaseConfig.get_database_session()
        user = UserRepository.get_user_by_id(user_id, db)

        try:
            logger.info(f"Sending message to device {target_device_id}")

            device_message = {
                "message_type": "face_recognition",
                "message": f"User {user.first_name} {user.last_name} identified",
                "is_authenticated": True
            }

            message_sent = False
            attempt = 10
            while not message_sent and attempt > 0:
                try:
                    device_websocket = websocket_service.get_active_connections_dict().get(target_device_id)
                    await websocket_service.send_personal_message(device_message, device_websocket)
                    message_sent = True
                    logger.info(f"Message sent to device {target_device_id}")
                except Exception as ex:
                    logger.error(f"Error sending message to device {target_device_id}: {str(ex)}")
                    await asyncio.sleep(2)
                    attempt -= 1
            # update device status
            DeviceRepository.update_device_state(target_device_id, True, db)

            device_logs = DeviceLogs(
                device_id=target_device_id,
                log=f"User {user.first_name} {user.last_name} authenticated for device {target_device_id}",
                action="face_recognition",
            )

            DeviceLogsRepository.save(device_logs=device_logs, db=db)

            # save message to userlog
            user_logs = UserLogs(
                user_email=user.email,
                log=f"User {user.first_name} {user.last_name} authenticated on device {target_device_id}"
            )

            UserLogsRepository.save(user_logs, db)

            logger.info(f"Sending message to user {user.email}")
            user_websocket = websocket_service.get_active_connections_dict().get(user.email)
            user_message = {
                "message_type": "user_log",
                "message": f"User {user.first_name} {user.last_name} authenticated on device {target_device_id}",
                "email": user.email,
                "is_authenticated": True
            }
            await websocket_service.send_personal_message(user_message, user_websocket)
            logger.info(f"Message sent to user {user.email}")

        except Exception as ex:
            logger.error(f"Error sending message to user {user.email}: {str(ex)}")


    @classmethod
    def stop_process(cls, device_id):
        if device_id in streaming_devices:
            del streaming_devices[device_id]
            return True
        return False


    @classmethod
    def generate_message_frame(cls, message, color=(0, 0, 0)):
        frame = np.zeros((480, 720, 3), dtype=np.uint8)
        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2
        cv2.putText(frame, message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return frame


    @classmethod
    def video_feed(cls, device_id: str):
        def generate_frames():
            while True:
                if device_id in streaming_devices:
                    frame = streaming_devices[device_id]['frame']
                else:
                    frame = cls.generate_message_frame(f"Not available Stream for device {device_id}", (0, 0, 255))
                if frame is None:
                    continue

                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')
