
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from modules.cameras.models import Camera
from modules.vehicles.models import Vehicle
from modules.files.service import upload_file
from exceptions.models import CustomError
from utils.query_builder import query_builder
from modules.vehicles.utils import transform_vehicle_data
from websocket import active_connections
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone
import json
import asyncio


async def create_vehicle(db: AsyncSession, category : str, direction: str, len_violation:bool, speed_violation: int, speed:str, tracker_id:int, camera_id : int):
#      # checking for existence camera with the provided camera_id
    camera_result = await db.execute(select(Camera).where(Camera.id == camera_id).options(joinedload(Camera.road), joinedload(Camera.intersection), joinedload(Camera.zone)))
    camera = camera_result.scalar_one_or_none()
    if not camera:
     raise CustomError(message= "No camera found with this id", status_code=404, resolution="please provide valid camera_id")
    road_id= camera.road.id
    intersection_id= camera.intersection.id
    zone_id = camera.zone.id
     
      # making an instance of the Vehicle object that inherits from Vehicle Class (Models class)
    new_vehicle = Vehicle(category= category, direction= direction, len_violation=len_violation, speed_violation=speed_violation, speed=speed, tracker_id=tracker_id, camera_id=camera_id, road_id=road_id, intersection_id=intersection_id, zone_id=zone_id  )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)

    return {
          "id" : new_vehicle.id,
    }



async def update_vehicle_service(
    db: AsyncSession,
    vehicle_id: int,
    license_number: str,
    photos: dict[str, UploadFile]  # Receive dictionary of files
):
    # Fetch the vehicle from the database
    vehicle_result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id).options( joinedload(Vehicle.camera) ,joinedload(Vehicle.road), joinedload(Vehicle.intersection), joinedload(Vehicle.zone)))
    vehicle = vehicle_result.scalar_one_or_none()

    if not vehicle:
        raise CustomError(message="Vehicle not found", status_code=404, resolution="Provide a valid vehicle_id")

    # Update license number
    vehicle.license_number = license_number

    if photos.get("photo"):
        # read_photo = await photos["photo"].read()
        photo_file= photos.get("photo")
        uploaded_file = await upload_file(db=db, file=photo_file)
        url= uploaded_file["url"]
        vehicle.photo = url # will be link
    if photos.get("license_photo"):
        photo_file= photos.get("license_photo")
        uploaded_file = await upload_file(db=db, file=photo_file)
        url= uploaded_file["url"]
        vehicle.license_photo = url # will be link

    await db.commit()
    await db.refresh(vehicle)

    vehicle_data= transform_vehicle_data(vehicle)
    x = jsonable_encoder(vehicle_data)
    message= "new vehicle added"
    event_data = json.dumps({"event": "new-vehicle-added", "data": {"message": message, "data": x}})

    if active_connections:
        await asyncio.gather(*(ws.send_text(event_data) for ws in active_connections))

    return None


async def get_vehicles(db: AsyncSession, page:int, limit:int):
    filters= {} # Dynamic filters
    return await query_builder(
        db=db,
        model=Vehicle,
        filters=filters,
        page=page,
        limit=limit,
        relationships=[Vehicle.camera, Vehicle.road, Vehicle.intersection, Vehicle.zone],  # ✅ Joined load applied
        transform_fn=transform_vehicle_data  # ✅ Transform function applied
    )



async def get_vehicles_count_analysis(
    db: AsyncSession,
    camera_id: int
):
    # Get today's date range
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=999999)

    # Query to get category-wise count for today's entries and exits
    stmt = (
        select(
            Vehicle.category,
            func.count().filter(Vehicle.direction == "Entry").label("totalEntry"),
            func.count().filter(Vehicle.direction == "Exit").label("totalExit")
        )
        .where(Vehicle.camera_id == camera_id, Vehicle.created_at >= today_start, Vehicle.created_at <= today_end)
        .group_by(Vehicle.category)
    )

    result = await db.execute(stmt)
    vehicles_count = result.fetchall()
    # Calculate totalEntry and totalExit across all categories
    totalEntry = sum(row.totalEntry for row in vehicles_count)
    totalExit = sum(row.totalExit for row in vehicles_count)



    # Format the result
    response = [
        {
            "category": row.category,
            "totalEntry": row.totalEntry,
            "totalExit": row.totalExit
        }
        for row in vehicles_count
    ]
    
    return {"totalEntry": totalEntry, "totalExit": totalExit, "data": response}

    