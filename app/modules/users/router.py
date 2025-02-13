
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.users.schemas import UserCreateRequest,  UserCreateResponse
from modules.users.service import create_user
from database import get_db 
user_router = APIRouter()


@user_router.post("/add-user", response_model=UserCreateResponse)
async def add_user(user:UserCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_user(db= db, email= user.email, role=user.role, name=user.name, password=user.password, secret_key=user.secret_key)