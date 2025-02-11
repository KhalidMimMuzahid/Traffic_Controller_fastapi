
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.intersections.schemas import IntersectionCreateResponse, IntersectionCreate
from database import get_db 
from modules.intersections.service import create_intersection
intersection_router = APIRouter()
@intersection_router.post("/add-intersection", response_model=IntersectionCreateResponse)
async def add_zone(intersection: IntersectionCreate, db: AsyncSession = Depends(get_db)):
    return await create_intersection(db, intersection.name, intersection.zone_id )

# @router.get("/", response_model=list[ZoneResponse])
# async def list_zones(db: AsyncSession = Depends(get_db)):
#     return await get_zones(db)