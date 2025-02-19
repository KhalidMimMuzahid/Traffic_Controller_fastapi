from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")

class AIPolicingException(Exception):
    """This is the base class for all AIPolicing errors"""

    def __init__(self, status_code: int, message: str, resolution: str = None):
        self.status_code = status_code
        self.message = message
        self.resolution = resolution
        super().__init__(message)

class CustomError(AIPolicingException):
    """User has provided an invalid or expired token"""

    def __init__(self, status_code: int, message: str, resolution: str = None):
        super().__init__(status_code, message, resolution)
    def __str__(self):
        return f"CustomError(status_code={self.status_code}, message={self.message}, resolution={self.resolution})"





class ExceptionContent():
    is_success: bool = False
    error: Any = None
    def __init__(self, message: str, resolution: Optional[str]= "No resolution provided"):
        self.error = {
            "message": message,
            "resolution": resolution,
        }
    def to_dict(self):
        return {"is_success": self.is_success, "error": self.error}

    




# class Response(BaseModel, Generic[T]):
#     is_success: bool = True
#     message: str
#     data: T