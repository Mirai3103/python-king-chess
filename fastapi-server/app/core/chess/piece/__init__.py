from ..type import (
    PieceType,
    
)
from .bishop_strategy import BishopStrategy
from .king_strategy import KingStrategy
from .knight_strategy import KnightStrategy
from .pawn_strategy import PawnStrategy
from .queen_strategy import QueenStrategy
from .rook_strategy import RookStrategy
from .picece_strategy import PieceStrategy



PIECES_STRATEGY: dict[PieceType, PieceStrategy] = {
    PieceType.PAWN: PawnStrategy(),
    PieceType.KNIGHT: KnightStrategy(),
    PieceType.BISHOP: BishopStrategy(),
    PieceType.ROOK: RookStrategy(),
    PieceType.QUEEN: QueenStrategy(),
    PieceType.KING: KingStrategy(),
}

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
