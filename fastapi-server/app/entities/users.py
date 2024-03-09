from sqlalchemy import Boolean, Column, Integer, String
from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(length=100), unique=True, index=True)
    hashed_password = Column(String(length=100))
    is_active = Column(Boolean, default=True)

