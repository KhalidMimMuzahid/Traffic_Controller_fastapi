
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.intersections.models import Intersection
from modules.zones.models import Zone
from fastapi import HTTPException


async def create_intersection(db: AsyncSession, name: str, zone_id:int):
    zoneData = await db.execute(select(Zone).where(Zone.id == zone_id))
    has_exists_zone = zoneData.scalar_one_or_none()
    if not has_exists_zone:
         raise HTTPException(status_code=404, detail=f"Zone with ID {zone_id} not found.")
    
    #  making an instance of the intersection object that inherits from Intersection Class (Models class)
    intersection = Intersection(name=name, zone_id=zone_id)
    db.add(intersection)
    await db.commit()
    await db.refresh(intersection)
    
    return intersection

# async def get_zones(db: AsyncSession):
#     result = await db.execute(select(Zone))
#     return result.scalars().all()