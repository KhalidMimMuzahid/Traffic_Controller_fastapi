
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.cameras.schemas import CameraCreateRequest, CameraCreateResponse,CameraListResponse
from database import get_db 
from modules.cameras.service import create_camera, get_cameras
from responses.models import Response
from responses.handler import create_response
camera_router = APIRouter()


@camera_router.post("/add-camera"
, response_model=  Response[CameraCreateResponse]
)
async def add_camera(camera: CameraCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_camera(db=db, name= camera.name,direction_type= camera.direction_type, road_id=camera.road_id )
    return create_response(result=result, pydantic_model=CameraCreateResponse, message="Camera has created successfully")


@camera_router.get("/get-cameras",
 response_model= Response[list[CameraListResponse]]
 )
async def list_cameras(page:int=1, limit:int=10, road_id:int= None, db: AsyncSession = Depends(get_db)):
    result= await get_cameras(db, page=page, limit=limit, road_id=road_id)
    # return result
    return create_response(result=result["data"], pydantic_model=CameraListResponse, message="cameras have retrieved successfully", meta_data=result["meta_data"] )
    