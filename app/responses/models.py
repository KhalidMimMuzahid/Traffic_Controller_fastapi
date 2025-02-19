from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    is_success: bool = True
    message: str
    data: T


