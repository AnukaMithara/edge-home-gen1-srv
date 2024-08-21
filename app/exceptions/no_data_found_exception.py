from app.exceptions.base_exception import BaseAppException


class NoDataFoundException(BaseAppException):
    def __init__(self, results: str):
        super().__init__(is_error=True, results=results, message_template="requested {} object not found")
