from fastapi import FastAPI 
from routes.router import router
from database import init_db

app = FastAPI()

# If you want to automatically initialize your DB on startup,
# @app.on_event("startup")
# async def on_startup():
#     # This will run when the application starts and use the existing event loop.
#     await init_db()


# we are redirecting all routes to routes to handle easily
app.include_router(router, prefix="/api/v1")













