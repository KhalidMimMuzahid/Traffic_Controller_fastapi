
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.zones.schemas import ZoneResponse, ZoneCreate
from database import get_db 
from modules.zones.service import create_zone
zone_router = APIRouter()
@zone_router.post("/add-zone"
                #   , response_model=ZoneResponse
                  )
async def add_zone(zone: ZoneCreate, db: AsyncSession = Depends(get_db)):
    return await create_zone(db, zone.name)
# @router.get("/", response_model=list[ZoneResponse])
# async def list_zones(db: AsyncSession = Depends(get_db)):
#     return await get_zones(db)