
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, asc, func
import math
from modules.zones.models import Zone
from responses.models import MetaData
from utils.query_builder import query_builder
from exceptions.models import CustomError
from modules.intersections.models import Intersection



async def create_zone(db: AsyncSession, name: str):
    zone = Zone(name=name)
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone

async def get_zones(db: AsyncSession,page, limit, name):
    filters = {"name": name}  # Dynamic filters
    return await query_builder(db, Zone, filters, page, limit)

# async def delete_zone_service(db: AsyncSession, id:str):
#     zone = await db.query(Zone).filter(Zone.id == id).first()
#     if zone:
#         db.delete(zone)
#         await db.commit()
#         # if zone deleted the also delete intersection, camera, road etc 
#         return None
#     else:
#         raise CustomError(status_code=404, message= "no zone found with this it", resolution="please provide a valid zone id")


async def delete_zone_service(db: AsyncSession, id: str):
    # Use `select()` instead of `db.query()`
    result = await db.execute(select(Zone).filter(Zone.id == id))
    zone = result.scalars().first()  # Extract the first matching result
    if not zone:
        raise CustomError(
            status_code=404, 
            message="No zone found with this ID", 
            resolution="Please provide a valid zone ID"
        )
    # Fetch related entity
    intersections = await db.execute(select(Intersection).filter(Intersection.zone_id == id))
    cameras = await db.execute(select(Camera).filter(Camera.zone_id == id))




    if zone:
        await db.delete(zone)  # Correct way to delete in AsyncSession
        await db.commit()

        # If zone deleted, also delete related entities like intersection, camera, road, etc.
        return None
    else:
        raise CustomError(
            status_code=404, 
            message="No zone found with this ID", 
            resolution="Please provide a valid zone ID"
        )
