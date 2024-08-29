class DbOperationException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class ChatCompletionException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class DeletionException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class RestClientException(Exception):
    def __init__(self, message: str, status: int):
        self.status = status
        self.message = message


class NoDataFoundException(Exception):
    def __init__(self, message: str, status: int):
        self.status = status
        self.message = message


class UnauthorizedException(Exception):
    def __init__(self, message: str, status: int):
        self.status = status
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message: str, status: int):
        self.status = status
        self.message = message
