
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from modules.users.schemas import UserCreateRequest,  UserCreateResponse,UserLoggedInStatusResponse, UserLogInResponse, UsersListResponse
from modules.users.service import create_user, login_user_service,check_logged_in_status_service, get_users_service
from database import get_db 
from responses.handler import create_response
from responses.models import Response
from utils.validate_user_access_api import validate_user_access_api
user_router = APIRouter()



@user_router.post("/add-user", response_model=Response[UserCreateResponse])
async def add_user(request: Request,user:UserCreateRequest, db: AsyncSession = Depends(get_db)):
    # validating user to access this api 
    auth=request.state.user
    validate_user_access_api(auth=auth, access_users=["super_admin", "admin"])
    
    result =  await create_user(db= db, email= user.email, role=user.role, name=user.name, password=user.password, secret_key=user.secret_key)

    # Call the helper function to create the response and return it, passing UserCreateResponse model
    return create_response(result, UserCreateResponse, "User has created successfully")

@user_router.get("/login", response_model=Response[UserLogInResponse]
)
async def login_user(email:str, password:str, db: AsyncSession = Depends(get_db)):
    result= await login_user_service(db, email, password)
    return create_response(result, UserLogInResponse, "User has logged in successfully")

@user_router.get("/check_logged_in_status", response_model=Response[UserLoggedInStatusResponse]
)
async def check_logged_in_status(request: Request, db: AsyncSession = Depends(get_db)):
    auth=request.state.user
    result= await check_logged_in_status_service(db, auth)
    return create_response(result, UserLoggedInStatusResponse, "User authenticate successfully")

@user_router.get("/get-users"
, response_model=Response[list[UsersListResponse]]
)

async def get_users(page:int=1, limit:int=10, db: AsyncSession = Depends(get_db)):
    result= await get_users_service(page, limit, db)
    return create_response(result["data"], UsersListResponse, "Users have retrieved successfully", result["meta_data"] )