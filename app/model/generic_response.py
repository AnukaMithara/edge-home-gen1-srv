from typing import Optional, Any


class GenericResponse:
    def __init__(self, is_error: bool, message: str, results: Optional[Any]):
        self.is_error = is_error
        self.message = message
        self.results = results

    @classmethod
    def success(cls, message: str, results: Optional[Any] = None):
        return cls(is_error=False, message=message, results=results)

    @classmethod
    def failed(cls, message: str, results: Optional[Any]):
        return cls(is_error=True, message=message, results=results)
