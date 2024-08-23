import os

from app.entity.user import User
from fastapi import UploadFile
from typing import List
from PIL import Image

from app.entity.user_logs import UserLogs
from app.model.user_model import UserModel
from app.model.generic_response import GenericResponse
from app.config.logging_config import get_logger
from app.repository.user_logs_repository import UserLogsRepository
from app.repository.user_repository import UserRepository
from app.service.image_embedding_service import ImageEmbeddingService
from app.util.util import encrypt_password, decrypt_password

logger = get_logger(class_name=__name__)


class UserService:

    @classmethod
    def create_user(cls, user: UserModel, image_list: List[UploadFile], db):
        image_paths = []
        try:
            logger.info("Create User Process Started")

            for image in image_list:
                try:
                    img = Image.open(image.file)
                    img.verify()
                except Exception as e:
                    return GenericResponse.failed(message=f"Invalid image file: {image.filename}. Error: {str(e)}",
                                                  results=[])

                image_path = f"temp/{image.filename}"
                image.file.seek(0)
                if not os.path.exists("temp"):
                    os.makedirs("temp")
                with open(image_path, "wb") as buffer:
                    buffer.write(image.file.read())
                image_paths.append(image_path)

            user_entity = User(
                email=user.email,
                password=encrypt_password(user.password),
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
                role=user.role,
                is_active=True,
                is_verified=False
            )

            saved_user = UserRepository.save(user_entity, db)

            user_logs = UserLogs(
                user_email=saved_user.email,
                log=f"User {saved_user.email} created"
            )

            UserLogsRepository.save(user_logs, db)

            face_data_results = ImageEmbeddingService.store_embedding_in_db(user_id=saved_user.id, img_list=image_paths,
                                                                            db=db)

            results = {
                "id": saved_user.id,
                "email": saved_user.email,
                "first_name": saved_user.first_name,
                "last_name": saved_user.last_name,
                "phone_number": saved_user.phone_number,
                "role": saved_user.role,
                "is_active": saved_user.is_active,
                "is_verified": saved_user.is_verified,
                "face_data": face_data_results
            }

            logger.info("Create User Process End")
            return GenericResponse.success(message="Create User Success", results=results)
        except Exception as ex:
            logger.error(f"Create User Error: {str(ex)}")
            logger.info("Create User End With Error")
            return GenericResponse.failed(message=f"Create User Failed, Error: {str(ex)}", results=[])
        finally:
            for image_path in image_paths:
                try:
                    os.remove(image_path)
                except OSError as e:
                    logger.error(f"Error deleting temp file {image_path}: {e}")

    @classmethod
    def login_user(cls, login_model, db):
        try:
            logger.info("Login User Process Started")

            user = UserRepository.get_user_by_email(email=login_model.email, db=db)
            if not user:
                logger.info("Login User Process End with error")
                return GenericResponse.failed(message="Unauthorized user", results=[], status_code=401)

            if decrypt_password(user.password) != login_model.password:
                logger.info("Login User Process End")
                return GenericResponse.failed(message="Invalid password", results=[])

            user_dict = user.__dict__
            user_dict.pop('password')

            logger.info("Login User Process End")
            return GenericResponse.success(message="Login Success", results=user_dict)
        except Exception as ex:
            logger.error(f"Login User Error: {str(ex)}")
            logger.info("Login User End With Error")
            return GenericResponse.failed(message=f"Login Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_user_by_email(cls, email, db):
        try:
            logger.info("Get User Process Started")

            user = UserRepository.get_user_by_email(email=email, db=db)
            if not user:
                logger.info("Get User Process End with error")
                return GenericResponse.failed(message="User not found", results=[], status_code=404)

            user_dict = user.__dict__
            user_dict.pop('password')

            logger.info("Get User Process End")
            return GenericResponse.success(message="User found", results=user_dict)
        except Exception as ex:
            logger.error(f"Get User Error: {str(ex)}")
            logger.info("Get User End With Error")
            return GenericResponse.failed(message=f"Get User Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_all_users(cls, db):
        try:
            logger.info("Get All Users Process Started")

            users = db.query(User).all()
            users_list = []
            for user in users:
                user_dict = user.__dict__
                user_dict.pop('password')
                users_list.append(user_dict)

            logger.info("Get All Users Process End")
            return GenericResponse.success(message="Users found", results=users_list)
        except Exception as ex:
            logger.error(f"Get All Users Error: {str(ex)}")
            logger.info("Get All Users End With Error")
            return GenericResponse.failed(message=f"Get All Users Failed, Error: {str(ex)}", results=[])

    @classmethod
    def verify_user(cls, email, db):
        try:
            logger.info("Verify User Process Started")

            user = UserRepository.get_user_by_email(email=email, db=db)
            if not user:
                logger.info("Verify User Process End with error")
                return GenericResponse.failed(message="User not found", results=[], status_code=404)

            user.is_verified = True
            UserRepository.save(user, db)

            user_logs = UserLogs(
                user_email=user.email,
                log=f"User {user.email} verified"
            )

            UserLogsRepository.save(user_logs, db)

            logger.info("Verify User Process End")
            return GenericResponse.success(message="User verified", results=[])
        except Exception as ex:
            logger.error(f"Verify User Error: {str(ex)}")
            logger.info("Verify User End With Error")
            return GenericResponse.failed(message=f"Verify User Failed, Error: {str(ex)}", results=[])
