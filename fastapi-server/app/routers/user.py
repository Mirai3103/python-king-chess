from fastapi import APIRouter, Depends

from app.dtos.user_dto import UserCreate, UserBase
from app.services.user_service import UserService

UserRouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

@UserRouter.get("/", response_model=list[UserBase])
async def index(userservice: UserService = Depends(UserService)):
     print('hhh')
     return  userservice.get_all_users()
  
@UserRouter.get("/{user_id}", response_model=UserBase)
async def get_user(user_id: int,userservice: UserService = Depends(UserService)):
    return userservice.get_user(user_id)

@UserRouter.post("/", response_model=UserBase)
async def create_user(user: UserCreate,userservice: UserService = Depends(UserService)):
    return userservice.create_user(user)

     

