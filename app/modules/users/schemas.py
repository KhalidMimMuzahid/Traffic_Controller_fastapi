from pydantic import BaseModel
from enum import Enum




# Define an enumeration for Role
class UserRoleEnum(str, Enum):
    admin = "admin"
    super_admin = "super_admin"

class UserCreateRequest(BaseModel):
    email :str
    role : UserRoleEnum
    name :str
    password :str
    secret_key :str

class UserCreateResponse(BaseModel):
    id: int
    email :str
    role : UserRoleEnum
    name :str
    # password :str
    # secret_key :str
    class Config:
        orm_mode = True
        extra = "ignore"  # This will ignore any extra fields (like "password")

