from pydantic import BaseModel
from modules.zones.schemas import ZoneReferenceResponseForCreateIntersection

class IntersectionCreateRequest(BaseModel):
    name: str
    zone_id: int



class IntersectionCreateResponse(BaseModel):
    id: int
    name: str
    zone: ZoneReferenceResponseForCreateIntersection
    class Config:
        orm_mode = True



class IntersectionListResponse(IntersectionCreateResponse):
    # extra_field: str  # Add extra fields if needed
    pass

class IntersectionReferenceResponseForCreateRoad(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
        extra = "ignore"

class IntersectionReferenceResponseForCreateCamera(IntersectionReferenceResponseForCreateRoad):
    pass

class IntersectionReferenceResponseForCreateVehicle(IntersectionReferenceResponseForCreateRoad):
    pass


