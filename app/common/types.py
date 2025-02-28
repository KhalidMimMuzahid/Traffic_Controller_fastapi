from enum import Enum
from typing import List, Dict, Union


# Define an enumeration for Role
class UserRoleEnum(str, Enum):
    admin = "admin"
    super_admin = "super_admin"

# Define the authentication dictionary type
TAuth = Dict[str, Union[str, UserRoleEnum]]