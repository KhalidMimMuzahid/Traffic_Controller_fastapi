from fastapi import APIRouter
from modules.zones.router import zone_router
from modules.intersections.router import intersection_router

# creating a router 
router = APIRouter()

# calling a router depends on prefix
router.include_router(zone_router, prefix="/zones", tags=["Zones"])
router.include_router(intersection_router, prefix="/intersections", tags=["Intersections"])