
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.cameras.models import Camera
from modules.cameras.schemas import DirectionTypeEnum, CameraResponse
from modules.zones.models import Zone
from modules.intersections.models import Intersection

from fastapi import HTTPException
async def create_camera(db: AsyncSession, name: str, road_no = int,road_name = str, direction_type= DirectionTypeEnum, intersection_id = int,zone_id = int):
     # checking for existence zone with the provided zone_id
    existing_zone = await db.execute(select(Zone).where(Zone.id == zone_id))
    has_exists_zone = existing_zone.scalar_one_or_none()

    if not has_exists_zone:
         raise HTTPException(status_code=404, detail=f"Zone with ID {zone_id} not found.")
    # checking for existence intersection with the provided intersection_id
    existing_intersection = await db.execute(select(Intersection).where(Intersection.id == intersection_id))
    has_existing_intersection = existing_intersection.scalar_one_or_none()
    if not has_existing_intersection:
         raise HTTPException(status_code=404, detail=f"Intersection with ID {intersection_id} not found.")
    
    #  making an instance of the camera object that inherits from Camera Class (Models class)
    new_camera = Camera(name=name, road_no=road_no, road_name=road_name, direction_type=direction_type, intersection_id=intersection_id, zone_id=zone_id)
    print({'camera': new_camera})
    db.add(new_camera)
    await db.commit()
    await db.refresh(new_camera)
    return new_camera


async def get_cameras(db: AsyncSession):
    result = await db.execute(select(Camera).options(joinedload(Camera.intersection), joinedload(Camera.zone)))
    cameras=  result.scalars().all() 

    return cameras
#     return [
#         CameraResponse(
#             id=camera.id,
#             name= camera.name,
#             road_no=camera.road_no,
#             road_name=camera.road_name,
#             direction_type=camera.direction_type,
#             intersection_name=camera.intersection.name,  # Fetch the intersection name
#             zone_name=camera.zone.name,  # Fetch the zone name
#         )
#         for camera in cameras
#     ]
