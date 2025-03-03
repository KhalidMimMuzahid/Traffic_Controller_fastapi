
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from modules.zones.schemas import ZoneCreateRequest, ZoneCreateResponse, ZoneListResponse
from database import get_db 
from modules.zones.service import create_zone, get_zones
from responses.handler import create_response
from responses.models import Response
zone_router = APIRouter()
@zone_router.post("/add-zone", response_model=Response[ZoneCreateResponse])
async def add_zone(request: Request,zone: ZoneCreateRequest, db: AsyncSession = Depends(get_db)):
    result= await create_zone(db, zone.name)
    # Call the helper function to create the response and return it, passing UserCreateResponse model
    return create_response(result, ZoneCreateResponse, "Zone has created successfully")

@zone_router.get("/get-zones"
# , response_model=Response[list[ZoneListResponse]]
)
async def list_zones(page:int=1, limit:int=10, name:str=None, db: AsyncSession = Depends(get_db)):
    result= await get_zones(db, page, limit, name)
    # Call the helper function to create the response and return it, passing UserCreateResponse model
    return create_response(result["data"], ZoneListResponse, "Zones have retrieved successfully", result["meta_data"] )
    
    


