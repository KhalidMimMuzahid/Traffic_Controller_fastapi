from pydantic import BaseModel


class IntersectionCreate(BaseModel):
    name: str
    zone_id: int

class IntersectionResponse(IntersectionCreate):
    id: int
    class Config:
        orm_mode = True


