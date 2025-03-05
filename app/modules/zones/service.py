
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, asc, func
import math
from modules.zones.models import Zone
from responses.models import MetaData
from utils.query_builder import query_builder
from exceptions.models import CustomError
from modules.intersections.models import Intersection
from modules.cameras.models import Camera
from modules.roads.models import Road



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
    roads = await db.execute(select(Road).filter(Road.zone_id == id))

    # Convert scalars to lists
    intersections = intersections.scalars().all()
    cameras = cameras.scalars().all()
    roads = roads.scalars().all()

    # Delete all related entities
    for entity in intersections + cameras + roads:
        await db.delete(entity)

    # Delete the zone itself
    await db.delete(zone)
    await db.commit()
    return None