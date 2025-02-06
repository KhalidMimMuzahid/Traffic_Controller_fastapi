from pydantic import BaseModel


class ZoneCreate(BaseModel):
    name: str

class ZoneResponse(ZoneCreate):
    id: int
    class Config:
        orm_mode = True


