from pydantic import BaseModel
from enum import Enum
from modules.zones.schemas import ZoneReferenceResponseForCreateRoad
from modules.intersections.schemas import IntersectionReferenceResponseForCreateRoad


class RoadCreateRequest(BaseModel):
    name : str
    road_no : int
    intersection_id : int
    # zone_id : int

class RoadCreateResponse(BaseModel):
    id: int
    name : str
    road_no : int
    zone : ZoneReferenceResponseForCreateRoad
    intersection : IntersectionReferenceResponseForCreateRoad
    class Config:
        orm_mode = True
        extra = "ignore"


# class CameraListResponse(CameraCreateResponse):
#     # extra_field: str  # Add extra fields if needed
#     pass


# class IntersectionReferenceResponseForCreateVehicle(BaseModel):
#     id: int
#     name : str
#     road_no : int
#     road_name : str
#     direction_type: DirectionTypeEnum



class RoadReferenceResponseForCreateCamera(BaseModel):
    id: int
    name: str

class RoadReferenceResponseForCreateVehicle(RoadReferenceResponseForCreateCamera):
    pass

