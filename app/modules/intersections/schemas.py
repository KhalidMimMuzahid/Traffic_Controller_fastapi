from pydantic import BaseModel
from modules.zones.schemas import ZoneReferenceResponseForCreateIntersection

class IntersectionCreate(BaseModel):
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

# class IntersectionListResponse(BaseModel):
#     id: int
#     name: str
#     zone: ZoneReferenceResponseForCreateIntersection
#     class Config:
#         orm_mode = True
