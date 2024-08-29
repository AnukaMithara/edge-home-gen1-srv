import pickle
from datetime import datetime
from deepface import DeepFace
from app.config.logging_config import get_logger
from app.entity.user_face_data import UserFaceData
from app.repository.user_face_data_repository import UserFaceDataRepository

logger = get_logger(class_name=__name__)


class ImageEmbeddingService:

    @classmethod
    def generate_embedding(cls, image_path):
        logger.info(f"Generate embedding for image: {image_path}")
        embedding_data = DeepFace.represent(img_path=image_path, model_name="Facenet")[0]["embedding"]
        logger.info("Embedding generated successfully")
        return embedding_data

    @classmethod
    def store_embedding_in_db(cls, user_id, img_list: list, db):
        try:
            logger.info(f"Store embedding for user ID: {user_id}")
            results = []
            for img in img_list:
                embedding_data = cls.generate_embedding(img)
                user_face_data = UserFaceData(
                    user_id=user_id,
                    face_data=pickle.dumps(embedding_data),
                    created_at=datetime.now()
                )
                saved_data = UserFaceDataRepository.save(user_face_data, db)
                results.append({
                    "id": saved_data.id,
                })

            logger.info(f"Embeddings stored successfully for user ID: {user_id}")
            return results
        except Exception as ex:
            logger.error(f"Store embedding error: {str(ex)}")
            return []
