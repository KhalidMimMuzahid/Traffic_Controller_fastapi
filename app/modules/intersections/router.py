
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreate
from database import get_db 
from modules.intersections.service import create_intersection, get_intersections
intersection_router = APIRouter()
@intersection_router.post("/add-intersection", response_model=IntersectionCreateResponse)
async def add_zone(intersection: IntersectionCreate, db: AsyncSession = Depends(get_db)):
    return await create_intersection(db, intersection.name, intersection.zone_id )

@intersection_router.get("/get-intersections", response_model=list[IntersectionListResponse])
async def list_intersections(db: AsyncSession = Depends(get_db)):
    intersections= await get_intersections(db)
    return intersections