
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreateRequest
from database import get_db 
# from modules.intersections.service import create_intersection, get_intersections, delete_intersection_service
# from responses.handler import create_response
# from responses.models import Response
file_router = APIRouter()
from modules.files.service import get_file_service



@file_router.get("/get"
# , response_model=Response[list[IntersectionListResponse]]
)
async def get_file( id:str,db: AsyncSession = Depends(get_db)):
    result= await get_file_service(db, id=id)
    return result
    # return create_response(result=result["data"], pydantic_model=IntersectionListResponse, message="intersections have retrieved successfully", meta_data=result["meta_data"])


