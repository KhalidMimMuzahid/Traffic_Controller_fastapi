from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from modules.vehicles.schemas import VehicleCreateRequest, VehicleCreateResponse, VehicleListResponse, VehicleUpdateRequest
from database import get_db 
from modules.vehicles.service import create_vehicle, get_vehicles, update_vehicle_service
from responses.handler import create_response
from responses.models import Response
vehicle_router = APIRouter()




@vehicle_router.post("/add-vehicle", response_model=Response[VehicleCreateResponse])
async def add_vehicle(vehicle: VehicleCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_vehicle(db=db, category= vehicle.category , direction_type=  vehicle.direction_type, len_violation=vehicle.len_violation, speed_violation=vehicle.speed_violation, speed=vehicle.speed, tracker_id=vehicle.tracker_id, camera_id= vehicle.camera_id)
    return create_response(result=result, pydantic_model=VehicleCreateResponse, message="Vehicle has added successfully")



@vehicle_router.put("/update-vehicle/{vehicle_id}"
                    # , response_model=Response[VehicleCreateResponse]
                    )
async def update_vehicle(
    vehicle_id: int,
    license_number: str = Form(...),
    photo: UploadFile = File(None),  # Main vehicle photo
    license_photo: UploadFile = File(None),  # License plate photo
    db: AsyncSession = Depends(get_db),
):
    photos={
        "photo": photo,
        "license_photo": license_photo,
    }
    # Remove None values before passing to service
    photos = {key: file for key, file in photos.items() if file is not None}
    result = await update_vehicle_service(
        db=db,
        vehicle_id=vehicle_id,
        license_number=license_number,
        photos=photos
    )
    # return result
    return create_response(result=result, pydantic_model=VehicleUpdateRequest, message="Vehicle updated successfully")


@vehicle_router.get("/get-vehicles",
 response_model= Response[list[VehicleListResponse]]
 )
async def list_vehicles(page:int=1, limit:int=10, db: AsyncSession = Depends(get_db)):
    result= await get_vehicles(db, page=page, limit=limit)
    # return result
    return create_response(result=result["data"], pydantic_model=VehicleListResponse, message="vehicles have retrieved successfully", meta_data=result["meta_data"] )
    