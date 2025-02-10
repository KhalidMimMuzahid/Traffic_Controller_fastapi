from fastapi import FastAPI 
from routes.router import router


app = FastAPI()
app.include_router(router, prefix="/api/v1")













