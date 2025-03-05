
from fastapi import APIRouter, Depends
from modules.roads.schemas import RoadCreateRequest
from modules.roads.service import create_road, get_roads
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db 
from modules.roads.schemas import RoadCreateResponse, RoadListResponse
from responses.models import Response
from responses.handler import create_response

road_router = APIRouter()


@road_router.post("/add-road"
, response_model=  Response[RoadCreateResponse]
)
async def add_road(road: RoadCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_road(db=db, name= road.name, road_no=road.road_no, intersection_id= road.intersection_id  )
    return create_response(result=result, pydantic_model=RoadCreateResponse, message="Road has created successfully")


@road_router.get("/get-roads"
# ,response_model=list[RoadListResponse]
)
async def list_roads(page:int=1, limit:int=10, intersection_id:int= None, db: AsyncSession = Depends(get_db)):
    result= await get_roads(db, page=page, limit=limit, intersection_id=intersection_id)
    return result
    # return create_response(result=result["data"], pydantic_model=RoadListResponse, message="roads have retrieved successfully", meta_data=result["meta_data"])