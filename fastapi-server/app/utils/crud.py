from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db_connection

from ..entities.users import User

class CRUDUser:
    db: Session
    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db
    def create_user(self, user: User)-> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    def get_user(self, user_id: int)-> User:
        return self.db.query(User).filter(User.id == user_id).first()
    def get_all_users(self)-> list:
        return self.db.query(User).all()