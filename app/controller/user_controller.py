from fastapi import APIRouter, Response, UploadFile, File, Form
from typing import List

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.model.user_model import UserModel
from app.model.login_model import LoginModel
from app.service.user_service import UserService

router = APIRouter(
    prefix="/v1/user",
    tags=["User"]
)
logger = get_logger(class_name=__name__)
user_service = UserService()


@router.post("/create")
async def create_user(db: db_dependency, response: Response,
                email: str = Form(...),
                password: str = Form(...),
                first_name: str = Form(...),
                last_name: str = Form(...),
                phone_number: str = Form(...),
                role: str = Form(...),
                image_list: List[UploadFile] = File(...)):
    user = UserModel(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        role=role
    )
    result = user_service.create_user(user=user, image_list=image_list, db=db)
    response.status_code = result.status_code
    return result


@router.post("/login")
async def login_user(db: db_dependency, response: Response, login_model: LoginModel):
    result = user_service.login_user(login_model=login_model, db=db)
    response.status_code = result.status_code
    return result


@router.get("/get/{email}")
async def get_user_by_email(db: db_dependency, response: Response, email: str):
    result = user_service.get_user_by_email(email=email, db=db)
    response.status_code = result.status_code
    return result

@router.get("/all")
async def get_all_users(db: db_dependency, response: Response):
    result = user_service.get_all_users(db=db)
    response.status_code = result.status_code
    return result

@router.get("/verify/{email}")
async def verify_user(db: db_dependency, response: Response, email: str):
    result = user_service.verify_user(email=email, db=db)
    response.status_code = result.status_code
    return result







