

from app.core.chess.chess import Chess
from ..type import InternalMove
from .picece_strategy import PieceStrategy

class KnightStrategy(PieceStrategy):
    def get_moves(self, game: Chess, from_2d:tuple[int,int]) -> list[InternalMove]:
        pass
    def check_move(self, game: Chess, from_2d:tuple[int,int], to_2d:tuple[int,int]) -> InternalMove:
        pass