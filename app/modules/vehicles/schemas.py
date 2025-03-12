from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from modules.cameras.schemas import CameraReferenceResponseForCreateVehicle
from modules.roads.schemas import RoadReferenceResponseForCreateVehicle
from modules.intersections.schemas import IntersectionReferenceResponseForCreateVehicle
from modules.zones.schemas import ZoneReferenceResponseForCreateVehicle


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



class VehicleListResponse(BaseModel):
    id: int
    category : str
    direction_type: DirectionTypeEnum
    len_violation: bool
    speed_violation: bool
    speed:int
    tracker_id: int
    license_number : str

    camera: CameraReferenceResponseForCreateVehicle
    road : RoadReferenceResponseForCreateVehicle
    intersection : IntersectionReferenceResponseForCreateVehicle
    zone : ZoneReferenceResponseForCreateVehicle
    created_at: datetime
    class Config:
        orm_mode = True
        extra = "ignore"
