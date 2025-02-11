
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.intersections.models import Intersection
from modules.intersections.schemas import IntersectionListResponse
from modules.zones.models import Zone
from fastapi import HTTPException


async def create_intersection(db: AsyncSession, name: str, zone_id:int):
    zone_result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = zone_result.scalar_one_or_none()
    if not zone:
         raise HTTPException(status_code=404, detail=f"Zone with ID {zone_id} not found.")
    
    #  making an instance of the intersection object that inherits from Intersection Class (Models class)
    intersection = Intersection(name=name, zone_id=zone_id)
    db.add(intersection)
    await db.commit()
    await db.refresh(intersection)
    
    return {
         "id": intersection.id,
         "name": intersection.name,
         "zone": zone
    }

async def get_intersections(db: AsyncSession):
    result = await db.execute(select(Intersection).options(joinedload(Intersection.zone)))
    intersections=  result.scalars().all()
    return intersections

