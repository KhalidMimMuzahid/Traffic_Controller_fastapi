from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from routes.router import router
from database import init_db
from exceptions.handler import register_all_errors
from dependencies.authenticate_user import authenticate_user
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# # If you want to automatically initialize your DB on startup,
@app.on_event("startup")
async def on_startup():
    # This will run when the application starts and use the existing event loop.
    await init_db()


# we are redirecting all routes to routes to handle easily
app.include_router(router, prefix="/api/v1", dependencies=[Depends(authenticate_user)])

register_all_errors(app)











