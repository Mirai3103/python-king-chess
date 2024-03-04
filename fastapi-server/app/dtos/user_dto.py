
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from app.database.database import Base, engine


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)


from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    id: int
    is_active: bool
    class Config:
        orm_mode = True
        from_attributes = True
    

class UserCreate(BaseModel):
    password: str
    email: str

