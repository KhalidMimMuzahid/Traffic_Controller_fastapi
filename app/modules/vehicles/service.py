
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.vehicles.schemas import DirectionTypeEnum
from modules.cameras.models import Camera
# from fastapi import HTTPException
from modules.vehicles.models import Vehicle
# from modules.roads.schemas import RoadReferenceResponseForCreateCamera
# from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera
# from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from exceptions.models import CustomError
# from utils.query_builder import query_builder
# from modules.cameras.utils import transform_camera_data



async def create_vehicle(db: AsyncSession, category : str, direction_type: DirectionTypeEnum, license_number: str, len_violation:bool, speed_violation: int, speed:int, tracker_id:int, camera_id : int):
#      # checking for existence camera with the provided camera_id
    camera_result = await db.execute(select(Camera).where(Camera.id == camera_id).options(joinedload(Camera.road), joinedload(Camera.intersection), joinedload(Camera.zone)))
    camera = camera_result.scalar_one_or_none()
    if not camera:
     raise CustomError(message= "No camera found with this id", status_code=404, resolution="please provide valid camera_id")
    road_id= camera.road.id
    intersection_id= camera.intersection.id
    zone_id = camera.zone.id
     
      # making an instance of the Vehicle object that inherits from Vehicle Class (Models class)
    new_vehicle = Vehicle(category= category, direction_type= direction_type, license_number=license_number, len_violation=len_violation, speed_violation=speed_violation, speed=speed, tracker_id=tracker_id, camera_id=camera_id, road_id=road_id, intersection_id=intersection_id, zone_id=zone_id  )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)

    return {
          "id" : new_vehicle.id,
 
    }


