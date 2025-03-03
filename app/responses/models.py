from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class MetaData(BaseModel):
    prev: Optional[int]  # Can be int or None
    next: Optional[int]  # Can be int or None
    current: int
    total: int # total number of pages depending on page limit
    class Config:
        orm_mode = True


class Response(BaseModel, Generic[T]):
    is_success: bool = True
    message: str
    data: T
    meta_data: Optional[MetaData]



# class MetaData:
#     def __init__(self, prev, next, current, total):
#         self.prev = prev
#         self.next = next
#         self.current = current
#         self.total = total

#     def to_dict(self):
#         return {
#             "prev": self.prev,
#             "next": self.next,
#             "current": self.current,
#             "total": self.total
#         }
