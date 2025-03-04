
from fastapi import APIRouter, Depends
from modules.roads.schemas import RoadCreateRequest
from modules.roads.service import create_road
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db 
from modules.roads.schemas import RoadCreateResponse
from modules.roads.schemas import RoadCreateResponse
from responses.models import Response
from responses.handler import create_response

road_router = APIRouter()
@road_router.post("/add-road"
, response_model=  Response[RoadCreateResponse]
)
async def add_road(road: RoadCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_road(db=db, name= road.name, road_no=road.road_no, intersection_id= road.intersection_id  )
    return create_response(result=result, pydantic_model=RoadCreateResponse, message="Rod haas created successfully")
    # return result
    # , zone_id=road.zone_id 
# @camera_router.get("/get-cameras", response_model=list[CameraListResponse])
# async def list_zones(db: AsyncSession = Depends(get_db)):
#     return await get_cameras(db)