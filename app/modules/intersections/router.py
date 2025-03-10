
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreateRequest
from database import get_db 
from modules.intersections.service import create_intersection, get_intersections, delete_intersection_service
from responses.handler import create_response
from responses.models import Response
intersection_router = APIRouter()


@intersection_router.post("/add-intersection", response_model=Response[IntersectionCreateResponse])
async def add_zone(intersection: IntersectionCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_intersection(db, intersection.name, intersection.zone_id )
    return create_response(result=result, pydantic_model=IntersectionCreateResponse, message="intersections has created successfully")



@intersection_router.get("/get-intersections"
, response_model=Response[list[IntersectionListResponse]]
)
async def list_intersections(page:int=1, limit:int=10, zone_id:int= None,db: AsyncSession = Depends(get_db)):
    result= await get_intersections(db, page=page, limit=limit, zone_id=zone_id)
    # return intersections
    return create_response(result=result["data"], pydantic_model=IntersectionListResponse, message="intersections have retrieved successfully", meta_data=result["meta_data"])



@intersection_router.delete("/delete-intersection"
# , response_model=Response[list[ZoneListResponse]]
)
async def delete_intersection(id:int, db: AsyncSession = Depends(get_db)):
    result= await delete_intersection_service(db, id)
    # Call the helper function to create the response and return it, passing UserCreateResponse  model 
    return create_response(result=result,  message="Intersection has deleted successfully successfully" )
    