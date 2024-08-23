from app.model.generic_response import GenericResponse
from app.config.logging_config import get_logger
from app.repository.user_logs_repository import UserLogsRepository

logger = get_logger(class_name=__name__)


class UserLogsService:

    @classmethod
    def get_all_user_logs(cls, db):
        try:
            logger.info("Get All User Logs Process Started")

            user_logs = UserLogsRepository.get_all(db=db)

            logger.info("Get All User Logs Process End")
            return GenericResponse.success(message="User Logs fetched", results=user_logs)
        except Exception as ex:
            logger.error(f"Get All User Logs Error: {str(ex)}")
            logger.info("Get All User Logs End With Error")
            return GenericResponse.failed(message=f"Get All User Logs Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_user_logs_by_user_email(cls, user_email, db):
        try:
            logger.info("Get User Logs By User Email Process Started")

            user_logs = UserLogsRepository.get_user_logs_by_user_email(user_email=user_email, db=db)

            logger.info("Get User Logs By User Email Process End")
            return GenericResponse.success(message="User Logs fetched", results=user_logs)
        except Exception as ex:
            logger.error(f"Get User Logs By User Email Error: {str(ex)}")
            logger.info("Get User Logs By User Email End With Error")
            return GenericResponse.failed(message=f"Get User Logs By User Email Failed, Error: {str(ex)}", results=[])
