
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.users.schemas import UserCreateRequest,  UserCreateResponse
from modules.users.service import create_user
from database import get_db 
from responses.handler import create_response
user_router = APIRouter()



@user_router.post("/add-user"
# , response_model=Response[UserCreateResponse]
)
async def add_user(user:UserCreateRequest, db: AsyncSession = Depends(get_db)):
    result =  await create_user(db= db, email= user.email, role=user.role, name=user.name, password=user.password, secret_key=user.secret_key)

    # Call the helper function to create the response and return it, passing UserCreateResponse model
    return create_response(result, UserCreateResponse, "User created successfully")

    
    # result_dict ={key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'}
    # user_response = UserCreateResponse(**result_dict)
    # return Response[UserCreateResponse](message="User created successfully", data=user_response)