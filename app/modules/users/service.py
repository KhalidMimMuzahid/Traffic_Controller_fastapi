
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.users.schemas import UserRoleEnum 
from modules.users.models import User
from exceptions.models import CustomError
from exceptions.models import CustomError
from utils.manage_auth import generate_passwd_hash, verify_password, create_access_token, decode_access_token
from utils.model_to_dict import model_to_dict



async def create_user(db: AsyncSession, email :str, role : UserRoleEnum, name :str, password :str, secret_key :str):
    
    # raise CustomError(status_code=401, message="xInvalid token", resolution="Please refresh your token.")
    
    password_hash= generate_passwd_hash(password)
    new_user = User(email =email,role =role,name =name,password =password_hash,secret_key =secret_key)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    if not new_user:
        raise CustomError(status_code=401, message="Something Went Wrong")
    return new_user


async def login_user_service(db: AsyncSession, email:str, password:str):
    result = await db.execute(select(User).where(User.email== email))
    user_data = result.scalars().first()
    if user_data is None:
        raise CustomError(status_code=401, message="no user found with this email", resolution= "enter a new email")
    password_is_valid = verify_password(password= password, hash= user_data.password)
    if not password_is_valid:
        raise CustomError(status_code=401, message="Invalid Password", resolution= "enter a correct password")
    access_token = create_access_token(
        user_data= {
            "id": user_data.id,
            "email": user_data.email,
            "role": user_data.role.value
        }
    )
    login_data = model_to_dict(user_data)
    login_data["access_token"] = access_token
    return login_data





