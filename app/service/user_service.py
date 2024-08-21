from app.entity.user import User
from app.model.user_model import UserModel
from app.model.generic_response import GenericResponse

from app.config.logging_config import get_logger
from app.repository.user_repository import UserRepository
from app.util.util import encrypt_password, decrypt_password

logger = get_logger(class_name=__name__)


class UserService:

    @classmethod
    def create_user(cls, user: UserModel, db):
        try:
            logger.info("Create User Process Started")
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

            results = saved_user.__dict__
            results.pop('password')

            logger.info("Create User Process End")
            return GenericResponse.success(message="Create User Success", results=results)
        except Exception as ex:
            logger.error(f"Create User Error: {str(ex)}")
            logger.info("Create User End With Error")
            return GenericResponse.failed(message=f"Create User Failed, Error: {str(ex)}", results=[])
