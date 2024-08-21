from pydantic import BaseModel


class UserModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    role: str

