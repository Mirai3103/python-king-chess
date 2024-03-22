from typing import Optional


from .picece_strategy import PieceStrategy


from ..type import   CellName, IChess, InternalMove, MoveType, Piece, PieceType

class BishopStrategy(PieceStrategy):
    def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> list[InternalMove]:
       moves = []
        return moves

    def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        return None