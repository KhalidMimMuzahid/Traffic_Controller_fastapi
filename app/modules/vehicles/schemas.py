from pydantic import BaseModel
from enum import Enum



class DirectionTypeEnum(str, Enum):
    entry = "entry"
    exit = "exit"

class VehicleCreateRequest(BaseModel):
    category : str
    direction_type: DirectionTypeEnum
    license_number: str

    len_violation:bool
    speed_violation: int
    speed:int
    tracker_id:int

    camera_id : int
class VehicleCreateResponse(BaseModel):
    id: int
    class Config:
        orm_mode = True
        extra = "ignore"