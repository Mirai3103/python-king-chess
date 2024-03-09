

from ..type import Board, Piece,InternalMove
from .picece_strategy import PieceStrategy

class KnightStrategy(PieceStrategy):
    def get_moves(self, board: Board, from_1d: int) -> list[InternalMove]:
        pass
    def check_move(self, board: Board[Piece], from_1d: int, to_1d: int) -> InternalMove:
        pass