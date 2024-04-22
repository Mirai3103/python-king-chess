from enum import Enum
from tokenize import String
from click import DateTime
from fastapi.datastructures import Default
from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.chess.type import CellName, InternalMove, PieceColor
from app.database.database import Base

class GameStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ABANDONED = 'abandoned'



class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True,autoincrement=True)
    black_name = Column(String, nullable=False)
    white_name = Column(String, nullable=False)
    winner_color = Column(Enum(PieceColor), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, Default=DateTime.now())
    moves = Column(JSON, nullable=False, Default=[])

    
    