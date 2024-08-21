class BaseAppException(Exception):
    def __init__(self, is_error: bool, results: str, message_template: str):
        self.is_error = is_error
        self.results = results
        self.message = message_template.format(results)

    def to_dict(self):
        return {"is_error": self.is_error, "message": self.message, "results": self.results}
