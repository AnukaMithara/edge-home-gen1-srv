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
