from fastapi import APIRouter
from modules.zones.router import zone_router
router = APIRouter()
router.include_router(zone_router, prefix="/zones", tags=["Zones"])