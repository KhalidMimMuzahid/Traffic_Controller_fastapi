
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreateRequest
from database import get_db 
from modules.intersections.service import create_intersection, get_intersections
from responses.handler import create_response
from responses.models import Response
intersection_router = APIRouter()
@intersection_router.post("/add-intersection", response_model=IntersectionCreateResponse)
async def add_zone(intersection: IntersectionCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_intersection(db, intersection.name, intersection.zone_id )

@intersection_router.get("/get-intersections"
, response_model=Response[list[IntersectionListResponse]]
)
async def list_intersections(page:int=1, limit:int=10, zone_id:int= None,db: AsyncSession = Depends(get_db)):
    result= await get_intersections(db, page=page, limit=limit, zone_id=zone_id)
    # return intersections
    return create_response(result=result["data"], pydantic_model=IntersectionListResponse, message="intersections have retrieved successfully", meta_data=result["meta_data"])