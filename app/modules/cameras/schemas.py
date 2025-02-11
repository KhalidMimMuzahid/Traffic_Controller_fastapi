from pydantic import BaseModel
from enum import Enum
from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera



class DirectionTypeEnum(str, Enum):
    entry = "entry"
    exit = "exit"

class CameraCreateRequest(BaseModel):
    name : str
    road_no : int
    road_name : str
    direction_type: DirectionTypeEnum
    intersection_id : int
    zone_id : int

class CameraCreateResponse(BaseModel):
    id: int
    name : str
    road_no : int
    road_name : str
    direction_type: DirectionTypeEnum
    zone : ZoneReferenceResponseForCreateCamera
    intersection : IntersectionReferenceResponseForCreateCamera
    class Config:
        orm_mode = True


class CameraListResponse(CameraCreateResponse):
    # extra_field: str  # Add extra fields if needed
    pass