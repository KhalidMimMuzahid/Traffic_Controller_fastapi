from fastapi import HTTPException, status
from enum import Enum
from typing import List, Union
from exceptions.models import CustomError
from common.types import TAuth, UserRoleEnum


def validate_user_access_api(auth: TAuth, access_users: Union[List[UserRoleEnum], str]):
    if access_users == "all":
        return  # Allow access
    elif auth["role"] in access_users:
        return  # Allow access
    else:
        raise CustomError(message= "You have no right to access this API", status_code=401)