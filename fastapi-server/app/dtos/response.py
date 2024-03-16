from typing import Optional


class Response:
    is_error: bool
    data: Optional[dict]
    message: Optional[str]

    def __init__(self, is_error: bool=False, data: Optional[dict] = None, message: Optional[str] = None):
        self.is_error = is_error
        self.data = data
        self.message = message

    def to_dict(self):
        return {
            "is_error": self.is_error,
            "data": self.data,
            "message": self.message
        }