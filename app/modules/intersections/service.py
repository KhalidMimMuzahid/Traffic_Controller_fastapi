
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.intersections.models import Intersection
from modules.intersections.schemas import IntersectionListResponse
from modules.zones.models import Zone
from fastapi import HTTPException
from modules.intersections.utils import transform_intersection_data
from utils.query_builder import query_builder
from exceptions.models import CustomError
from modules.cameras.models import Camera
from modules.roads.models import Road


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

async def get_intersections(db: AsyncSession, page:int, limit:int, zone_id:int):
#     result = await db.execute(select(Intersection).options(joinedload(Intersection.zone)))
#     intersections=  result.scalars().all()
#     return intersections
    filters= {"zone_id": zone_id} # Dynamic filters
    return await query_builder(
        db=db,
        model=Intersection,
        filters=filters,
        page=page,
        limit=limit,
        relationships=[Intersection.zone],  # ✅ Joined load applied
        transform_fn=transform_intersection_data  # ✅ Transform function applied
    )


async def delete_intersection_service(db: AsyncSession, id: str):
    # Use `select()` instead of `db.query()`
    result = await db.execute(select(Intersection).filter(Intersection.id == id))
    intersection = result.scalars().first()  # Extract the first matching result
    if not intersection:
        raise CustomError(
            status_code=404, 
            message="No intersection found with this ID", 
            resolution="Please provide a valid intersection ID"
        )
    # Fetch related entity
    cameras = await db.execute(select(Camera).filter(Camera.intersection_id == id))
    roads = await db.execute(select(Road).filter(Road.intersection_id == id))

    # Convert scalars to lists

    cameras = cameras.scalars().all()
    roads = roads.scalars().all()

    # Delete all related entities
    for entity in cameras + roads:
        await db.delete(entity)

    # Delete the intersection itself
    await db.delete(intersection)
    await db.commit()
    return None