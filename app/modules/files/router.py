
from fastapi import APIRouter, Depends, File, UploadFile, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
# from modules.intersections.schemas import IntersectionCreateResponse, IntersectionListResponse, IntersectionCreateRequest
from database import get_db 
# from modules.intersections.service import create_intersection, get_intersections, delete_intersection_service
# from responses.handler import create_response
# from responses.models import Response
from modules.files.service import get_file_service, upload_frame_service
from responses.handler import create_response
from modules.files.schemas import streamUpdateRequest

file_router = APIRouter()



@file_router.get("/get"
# , response_model=Response[list[IntersectionListResponse]]
)
async def get_file( id:str,db: AsyncSession = Depends(get_db)):
    result= await get_file_service(db, id=id)
    return result
    # return create_response(result=result["data"], pydantic_model=IntersectionListResponse, message="intersections have retrieved successfully", meta_data=result["meta_data"])


@file_router.post("/send-video-stream"
# , response_model=Response[list[IntersectionListResponse]]
)
async def upload_frame(camera_id: str = Form(...), file: UploadFile = File(...)):
    """Receive frame from Camera Server and store it by camera ID."""
    result = await upload_frame_service(camera_id= camera_id, file=file )

    return create_response(result=result, pydantic_model=streamUpdateRequest, message="stream updated successfully")



