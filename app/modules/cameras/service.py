
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.cameras.schemas import DirectionTypeEnum
# from modules.intersections.models import Intersection
from modules.cameras.models import Camera

from fastapi import HTTPException
from modules.roads.models import Road
from modules.roads.schemas import RoadReferenceResponseForCreateCamera
from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera
from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from exceptions.models import CustomError
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
          "road":RoadReferenceResponseForCreateCamera(**road.__dict__),
          "intersection" : IntersectionReferenceResponseForCreateCamera(**road.intersection.__dict__),
          "zone": ZoneReferenceResponseForCreateCamera(**road.zone.__dict__),
    }




#     # checking for existence intersection with the provided intersection_id
#     intersection_result = await db.execute(select(Intersection).where((Intersection.id == intersection_id) & (Intersection.zone_id == zone_id)))
#     intersection = intersection_result.scalar_one_or_none()
#     if not intersection:
#          raise HTTPException(status_code=404, detail=f"There have no Intersection with ID {intersection_id} in zone_id {zone_id}")
    
#     #  making an instance of the camera object that inherits from Camera Class (Models class)
#     new_camera = Camera(name=name, road_no=road_no, road_name=road_name, direction_type=direction_type, road_id=road_id, intersection_id=intersection_id, zone_id=zone_id)

#     db.add(new_camera)
#     await db.commit()
#     await db.refresh(new_camera)
#     return {
#           "id" : new_camera.id,
#           "name" : new_camera.name,
#           "road_no" : new_camera.road_no,
#           "road_name" : new_camera.road_name,
#           "direction_type" : new_camera.direction_type,
#           "zone": zone,
#           "intersection" : intersection,
#     }


async def get_cameras(db: AsyncSession):
    result = await db.execute(select(Camera).options(joinedload(Camera.intersection), joinedload(Camera.zone)))
    cameras=  result.scalars().all() 
    return cameras

