from pydantic import BaseModel


class ZoneCreateRequest(BaseModel):
    name: str

class ZoneCreateResponse(ZoneCreateRequest):
    id: int
    class Config:
        orm_mode = True

class ZoneListResponse(ZoneCreateResponse):
    # extra_field: str  # Add extra fields if needed
    pass

class ZoneReferenceResponseForCreateIntersection(BaseModel):
    id: int
    name: str

class ZoneReferenceResponseForCreateCamera(ZoneReferenceResponseForCreateIntersection):
    pass

class ZoneReferenceResponseForCreateVehicle(ZoneReferenceResponseForCreateIntersection):
    pass


