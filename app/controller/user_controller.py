from fastapi import APIRouter, Response

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.model.user_model import UserModel
from app.service.user_service import UserService

router = APIRouter(
    prefix="/v1/user",
    tags=["User"]
)
logger = get_logger(class_name=__name__)
user_service = UserService()


@router.post("/")
def create_user(response: Response, user: UserModel, db: db_dependency):
    result = user_service.create_user(user=user, db=db)
    response.status_code = result.status_code
    return result
