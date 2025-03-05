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
# class ZoneDeleteResponse(BaseModel):
#     data = None
#     class Config:
#         orm_mode = True

class ZoneReferenceResponseForCreateIntersection(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
        extra = "ignore"

class ZoneReferenceResponseForCreateRoad(ZoneReferenceResponseForCreateIntersection):
    class Config:
        orm_mode = True
        extra = "ignore"
    # pass

class ZoneReferenceResponseForCreateCamera(ZoneReferenceResponseForCreateIntersection):
    pass

class ZoneReferenceResponseForCreateVehicle(ZoneReferenceResponseForCreateIntersection):
    pass

