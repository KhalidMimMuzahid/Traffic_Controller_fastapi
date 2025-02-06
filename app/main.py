from fastapi import FastAPI 
from modules.zones.router import zone_router


app = FastAPI()
app.include_router(zone_router, prefix="/zones", tags=["Zones"])













