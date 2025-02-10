from pydantic import BaseModel
from enum import Enum



class DirectionTypeEnum(str, Enum):
    entry = "entry"
    exit = "exit"

class CameraCreate(BaseModel):
    name = str
    road_no = int
    road_name = str
    direction_type: DirectionTypeEnum
    intersection_id = int
    zone_id = int







class CameraResponse(CameraCreate):
    id: int
    class Config:
        orm_mode = True


