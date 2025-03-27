from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone, timedelta
from modules.cameras.schemas import CameraReferenceResponseForCreateVehicle
from modules.roads.schemas import RoadReferenceResponseForCreateVehicle
from modules.intersections.schemas import IntersectionReferenceResponseForCreateVehicle
from modules.zones.schemas import ZoneReferenceResponseForCreateVehicle



# BST = timezone(timedelta(hours=6))


class VehicleCreateRequest(BaseModel):
    category : str
    direction:str
    len_violation:bool
    speed_violation: bool
    speed:str
    tracker_id:int
    camera_id : int

class VehicleUpdateRequest(BaseModel):
    pass


class VehicleCreateResponse(BaseModel):
    id: int
    class Config:
        orm_mode = True
        extra = "ignore"



class VehicleListResponse(BaseModel):
    id: int
    category : str
    direction:str
    len_violation: bool
    speed_violation: bool
    speed:str
    tracker_id: int
    license_number : str
    photo: Optional[str] = None
    license_photo: Optional[str] = None
    license_number: Optional[str] = None

    camera: CameraReferenceResponseForCreateVehicle
    road : RoadReferenceResponseForCreateVehicle
    intersection : IntersectionReferenceResponseForCreateVehicle
    zone : ZoneReferenceResponseForCreateVehicle
    created_at: datetime
    class Config:
        orm_mode = True
        extra = "ignore"
   