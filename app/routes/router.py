from fastapi import APIRouter
from modules.zones.router import zone_router
from modules.intersections.router import intersection_router
from modules.cameras.router import camera_router
from modules.vehicles.router import vehicle_router
from modules.users.router import user_router
from modules.roads.router import road_router 
from modules.files.router import file_router
# middlewares
# creating a router 
router = APIRouter()

# calling a router depends on prefix
router.include_router(user_router, prefix="/users", tags=["Users"])  
router.include_router(zone_router, prefix="/zones", tags=["Zones"])
router.include_router(intersection_router, prefix="/intersections", tags=["Intersections"])  
router.include_router(road_router, prefix="/roads", tags=["Roads"])
router.include_router(camera_router, prefix="/cameras", tags=["Cameras"])  
router.include_router(vehicle_router, prefix="/vehicles", tags=["Vehicles"])  
router.include_router(file_router, prefix="/files", tags=["Files"])