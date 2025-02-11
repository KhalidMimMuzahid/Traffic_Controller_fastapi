
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cameras.schemas import CameraCreateRequest, CameraCreateResponse,CameraListResponse
from database import get_db 
from modules.cameras.service import create_camera, get_cameras
camera_router = APIRouter()
@camera_router.post("/add-camera", response_model=CameraCreateResponse)
async def add_camera(camera: CameraCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_camera(db=db, name= camera.name, road_no=camera.road_no, road_name=camera.road_name, direction_type= camera.direction_type, intersection_id= camera.intersection_id, zone_id=camera.zone_id  )
@camera_router.get("/get-cameras", response_model=list[CameraListResponse])
async def list_zones(db: AsyncSession = Depends(get_db)):
    return await get_cameras(db)