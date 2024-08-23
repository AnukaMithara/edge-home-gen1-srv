from fastapi import APIRouter, Response

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.service.user_logs_service import UserLogsService

router = APIRouter(
    prefix="/v1/user_logs",
    tags=["User Logs"]
)
logger = get_logger(class_name=__name__)
user_logs_service = UserLogsService()


@router.get("/all")
async def get_all_user_logs(db: db_dependency, response: Response):
    result = user_logs_service.get_all_user_logs(db=db)
    response.status_code = result.status_code
    return result


@router.get("/get/{user_email}")
async def get_user_logs_by_user_email(db: db_dependency, response: Response, user_email: str):
    result = user_logs_service.get_user_logs_by_user_email(user_email=user_email, db=db)
    response.status_code = result.status_code
    return result
