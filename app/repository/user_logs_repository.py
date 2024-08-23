from app.entity.user_logs import UserLogs
from app.exceptions.exception import DbOperationException


class UserLogsRepository:

    @classmethod
    def save(cls, user_log, db):
        try:
            db.add(user_log)
            db.commit()
            db.refresh(user_log)
            return user_log
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all(cls, db):
        try:
            return db.query(UserLogs).order_by(UserLogs.timestamp.desc()).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_user_logs_by_user_email(cls, user_email, db):
        try:
            return db.query(UserLogs).filter(UserLogs.user_email == user_email).order_by(
                UserLogs.timestamp.desc()).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)
