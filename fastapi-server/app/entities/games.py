from enum import Enum
from click import DateTime
from fastapi.datastructures import Default
from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database.database import Base

class GameStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ABANDONED = 'abandoned'



class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True,autoincrement=True)
    player1_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    player2_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    winner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(Enum(GameStatus), nullable=False,default=GameStatus.PENDING)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, Default=DateTime.now())
    moves = Column(JSON, nullable=False, Default=[])

    player1 = relationship('User', foreign_keys=[player1_id])
    player2 = relationship('User', foreign_keys=[player2_id])
    winner = relationship('User', foreign_keys=[winner_id])