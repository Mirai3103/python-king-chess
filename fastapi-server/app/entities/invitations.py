from enum import Enum
from unittest.mock import Base

from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Invitation(Base):
    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum('pending', 'accepted', 'rejected'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=DateTime.now())

    from_user = relationship('User', foreign_keys=[from_user_id])
    to_user = relationship('User', foreign_keys=[to_user_id])