from hmac import new
from fastapi import APIRouter, Depends

from app.dtos.user_dto import UserCreate, UserBase
from app.entities.users import User
from app.utils.crud import CRUDUser

UserRouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

@UserRouter.get("/", response_model=list[UserBase])
async def index(userCrud: CRUDUser = Depends(CRUDUser)):
     return  userCrud.get_all_users()
  
@UserRouter.get("/{user_id}", response_model=UserBase)
async def get_user(user_id: int, userCrud: CRUDUser = Depends(CRUDUser)):
    return userCrud.get_user(user_id)

@UserRouter.post("/", response_model=UserBase)
async def create_user(user: UserCreate, userCrud: CRUDUser = Depends(CRUDUser)):
    # // The `dict` method is deprecated; use `model_dump` instead.
    newUser =  User(**user.model_dump(
        exclude={"password"}
    ),    hashed_password = user.password)
    userCrud.create_user(newUser)

    return newUser

