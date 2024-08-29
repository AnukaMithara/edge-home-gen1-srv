from app.entity.user_face_data import UserFaceData
from app.exceptions.exception import DbOperationException
from app.entity.user import User

class UserFaceDataRepository:

    @classmethod
    def save(cls, user_face_data, db):
        try:
            db.add(user_face_data)
            db.commit()
            db.refresh(user_face_data)
            return user_face_data
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all(cls, db):
        try:
            return db.query(UserFaceData).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_verified_users(cls, db):
        try:
            return db.query(UserFaceData).join(User).filter(User.is_verified == True).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)