
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.cameras.schemas import DirectionTypeEnum
from modules.cameras.models import Camera
from fastapi import HTTPException
from modules.roads.models import Road
from modules.roads.schemas import RoadReferenceResponseForCreateCamera
from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera
from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from exceptions.models import CustomError
from utils.query_builder import query_builder
from modules.cameras.utils import transform_camera_data



async def create_camera(db: AsyncSession, name: str, direction_type= DirectionTypeEnum ,road_id = int):
     # checking for existence road with the provided road_id
    road_result = await db.execute(select(Road).where(Road.id == road_id).options(joinedload(Road.intersection), joinedload(Road.zone)))
    road = road_result.scalar_one_or_none()
    if not road:
     raise CustomError(message= "No road found with this id", status_code=404, resolution="please provide valid road_id")
    intersection_id= road.intersection.id
    zone_id = road.zone.id
     
     #  making an instance of the zone object that inherits from zone Class (Models class)
    new_camera = Camera(name=name, direction_type=direction_type, road_id= road.id, intersection_id=intersection_id, zone_id=zone_id)
    db.add(new_camera)
    await db.commit()
    await db.refresh(new_camera)

    return {
          "id" : new_camera.id,
          "name" :new_camera.name,
          "direction_type" : new_camera.direction_type,
          "road": RoadReferenceResponseForCreateCamera(**road.__dict__),
          "intersection" : IntersectionReferenceResponseForCreateCamera(**road.intersection.__dict__),
          "zone": ZoneReferenceResponseForCreateCamera(**road.zone.__dict__),
    }



async def get_cameras(db: AsyncSession, page:int, limit:int, road_id:int):
    filters= {"road_id": road_id} # Dynamic filters
    return await query_builder(
        db=db,
        model=Camera,
        filters=filters,
        page=page,
        limit=limit,
        relationships=[Camera.road, Camera.intersection, Camera.zone],  # ✅ Joined load applied
        transform_fn=transform_camera_data  # ✅ Transform function applied
    )


async def delete_camera_service(db: AsyncSession, id: str):
    # Use `select()` instead of `db.query()`
    result = await db.execute(select(Camera).filter(Camera.id == id))
    camera = result.scalars().first()  # Extract the first matching result
    if not camera:
        raise CustomError(
            status_code=404, 
            message="No camera found with this ID", 
            resolution="Please provide a valid camera ID"
        )
    # Delete the intersection itself
    await db.delete(camera)
    await db.commit()
    return None