
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.vehicles.schemas import VehicleCreateRequest, VehicleCreateResponse, VehicleListResponse
from database import get_db 
from modules.vehicles.service import create_vehicle, get_vehicles
from responses.handler import create_response
from responses.models import Response
vehicle_router = APIRouter()




@vehicle_router.post("/add-vehicle", response_model=Response[VehicleCreateResponse])
async def add_vehicle(vehicle: VehicleCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_vehicle(db=db, category= vehicle.category , direction_type=  vehicle.direction_type, license_number=vehicle.license_number, len_violation=vehicle.len_violation, speed_violation=vehicle.speed_violation, speed=vehicle.speed, tracker_id=vehicle.tracker_id, camera_id= vehicle.camera_id)
    return create_response(result=result, pydantic_model=VehicleCreateResponse, message="Vehicle has added successfully")



@vehicle_router.get("/get-vehicles",
 response_model= Response[list[VehicleListResponse]]
 )
async def list_vehicles(page:int=1, limit:int=10, db: AsyncSession = Depends(get_db)):
    result= await get_vehicles(db, page=page, limit=limit)
    # return result
    return create_response(result=result["data"], pydantic_model=VehicleListResponse, message="vehicles have retrieved successfully", meta_data=result["meta_data"] )
    