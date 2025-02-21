from fastapi import FastAPI , Depends
from routes.router import router
from database import init_db
from exceptions.handler import register_all_errors
from dependencies.authenticate_user import authenticate_user
app = FastAPI()

# If you want to automatically initialize your DB on startup,
@app.on_event("startup")
async def on_startup():
    # This will run when the application starts and use the existing event loop.
    await init_db()


# we are redirecting all routes to routes to handle easily
app.include_router(router, prefix="/api/v1", dependencies=[Depends(authenticate_user)])

register_all_errors(app)











