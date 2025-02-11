
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.zones.schemas import ZoneCreateRequest, ZoneCreateResponse, ZoneListResponse
from database import get_db 
from modules.zones.service import create_zone, get_zones
zone_router = APIRouter()
@zone_router.post("/add-zone", response_model=ZoneCreateResponse)
async def add_zone(zone: ZoneCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_zone(db, zone.name)

@zone_router.get("/get-zones", response_model=list[ZoneListResponse])
async def list_zones(db: AsyncSession = Depends(get_db)):
    return await get_zones(db)


