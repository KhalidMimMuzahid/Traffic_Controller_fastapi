from pydantic import BaseModel
from enum import Enum
from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera
from modules.roads.schemas import RoadReferenceResponseForCreateCamera



class DirectionTypeEnum(str, Enum):
    entry = "entry"
    exit = "exit"

class CameraCreateRequest(BaseModel):
    name : str
    direction_type: DirectionTypeEnum
    road_id : int

class CameraCreateResponse(BaseModel):
    id: int
    name : str
    direction_type: DirectionTypeEnum
    road : RoadReferenceResponseForCreateCamera
    intersection : IntersectionReferenceResponseForCreateCamera
    zone : ZoneReferenceResponseForCreateCamera
    class Config:
        orm_mode = True
        extra = "ignore"


class CameraListResponse(CameraCreateResponse):
    # extra_field: str  # Add extra fields if needed
    pass


class IntersectionReferenceResponseForCreateVehicle(BaseModel):
    id: int
    name : str
    road_no : int
    road_name : str
    direction_type: DirectionTypeEnum