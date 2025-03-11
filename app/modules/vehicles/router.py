
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.vehicles.schemas import VehicleCreateRequest, VehicleCreateResponse
from database import get_db 
from modules.vehicles.service import create_vehicle
from responses.handler import create_response
from responses.models import Response
vehicle_router = APIRouter()




@vehicle_router.post("/add-vehicle", response_model=Response[VehicleCreateResponse])
async def add_vehicle(vehicle: VehicleCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_vehicle(db=db, category= vehicle.category , direction_type=  vehicle.direction_type, license_number=vehicle.license_number, len_violation=vehicle.len_violation, speed_violation=vehicle.speed_violation, speed=vehicle.speed, tracker_id=vehicle.tracker_id, camera_id= vehicle.camera_id)
    return create_response(result=result, pydantic_model=VehicleCreateResponse, message="Vehicle has added successfully")

