
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.cameras.models import Camera
from modules.cameras.schemas import DirectionTypeEnum
from modules.zones.models import Zone
from modules.intersections.models import Intersection

from fastapi import HTTPException
async def create_camera(db: AsyncSession, name: str, road_no = int,road_name = str, direction_type= DirectionTypeEnum, intersection_id = int,zone_id = int):
     # checking for existence zone with the provided zone_id
    zone_result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = zone_result.scalar_one_or_none()

    if not zone:
         raise HTTPException(status_code=404, detail=f"Zone with ID {zone_id} not found.")
    # checking for existence intersection with the provided intersection_id
    intersection_result = await db.execute(select(Intersection).where((Intersection.id == intersection_id) & (Intersection.zone_id == zone_id)))
    intersection = intersection_result.scalar_one_or_none()
    if not intersection:
         raise HTTPException(status_code=404, detail=f"There have no Intersection with ID {intersection_id} in zone_id {zone_id}")
    
    #  making an instance of the camera object that inherits from Camera Class (Models class)
    new_camera = Camera(name=name, road_no=road_no, road_name=road_name, direction_type=direction_type, intersection_id=intersection_id, zone_id=zone_id)

    db.add(new_camera)
    await db.commit()
    await db.refresh(new_camera)
    return {
          "id" : new_camera.id,
          "name" : new_camera.name,
          "road_no" : new_camera.road_no,
          "road_name" : new_camera.road_name,
          "direction_type" : new_camera.direction_type,
          "zone": zone,
          "intersection" : intersection,
    }


async def get_cameras(db: AsyncSession):
    result = await db.execute(select(Camera).options(joinedload(Camera.intersection), joinedload(Camera.zone)))
    cameras=  result.scalars().all() 
    return cameras

