
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.users.schemas import UserRoleEnum
from modules.users.models import User
from exceptions.models import CustomError



async def create_user(db: AsyncSession, email :str,role : UserRoleEnum,name :str,password :str,secret_key :str):
    
    raise CustomError(status_code=401, message="xInvalid tokenx", resolution="Please refresh your token.")
    
    new_user = User(email =email,role =role,name =name,password =password,secret_key =secret_key)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    if not new_user:
        print("xx---------------------------------------------------------------------------")
        raise CustomError(status_code=401, message="Something Went Wrong")
    print("yy------------------------------------------------------------------------------")
    return new_user



