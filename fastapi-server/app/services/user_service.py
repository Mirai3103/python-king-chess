from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db_connection
from app.entities.users import User
from app.dtos.user_dto import UserCreate

class UserService:
    db: Session
    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db
    def get_user_by_email(self, email: str) -> Optional[User]:
        
        return self.db.query(User).filter(User.email == email).first()
    def create_user(self, user: UserCreate) -> User:
        newUser =  User(**user.model_dump(
        exclude={"password"}),    hashed_password = user.password)
        self.db.add(newUser)
        self.db.commit()
        self.db.refresh(newUser)
        return newUser
    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
    def update_user(self, user_id: int, user: UserCreate) -> User:
        user = self.get_user(user_id)
        for key, value in user.dict().items():
            if key in user.dict(exclude_unset=True):
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    