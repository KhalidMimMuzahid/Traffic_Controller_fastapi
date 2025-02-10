
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cameras.schemas import CameraCreate, CameraResponse
from database import get_db 
from modules.cameras.service import create_camera
intersection_router = APIRouter()
@intersection_router.post("/add-intersection"
                          # , response_model=CameraResponse
                          )
async def add_camera(camera: CameraCreate, db: AsyncSession = Depends(get_db)):
    return await create_camera(db=db, name= camera.name, road_no=camera.road_no, road_name=camera.road_name, direction_type= camera.direction_type, intersection_id= camera.intersection_id, zone_id=camera.zone_id  )
# @router.get("/", response_model=list[ZoneResponse])
# async def list_zones(db: AsyncSession = Depends(get_db)):
#     return await get_zones(db)