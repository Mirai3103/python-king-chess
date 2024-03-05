from ..type import PieceType
from .picece_strategy import  PieceStrategy

class PieceStrategyFactory:
    def __init__(self):
        self._strategies = {}

    def register(self, piece_type:PieceType, strategy:PieceStrategy):
        self._strategies[piece_type] = strategy

    def get_strategy(self, piece_type:PieceType)->PieceStrategy:
        return self._strategies[piece_type]
    

default_factory = PieceStrategyFactory()
    # # quân tốt 
    # PAWN = 'p' 
    # # quân mã
    # KNIGHT = 'n'
    # # quân tượng
    # BISHOP = 'b'
    # # quân xe
    # ROOK = 'r'
    # # quân hậu
    # QUEEN = 'q'
    # # quân vua
    # KING = 'k'
    # # ô trống
    # EMPTY = '0'