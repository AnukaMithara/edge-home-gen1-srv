from app.entity.user import User
from app.exceptions.exception import DbOperationException


class UserRepository:

    @classmethod
    def save(cls, user, db):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_user_by_email(cls, email, db):
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_user_by_id(cls, user_id, db):
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)
