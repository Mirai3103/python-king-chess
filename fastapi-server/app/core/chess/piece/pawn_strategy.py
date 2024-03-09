

from app.core.chess.chess import Chess
from ..type import Board, CellName, MoveType, Piece,InternalMove,PieceColor, PieceType
from .picece_strategy import PieceStrategy
# class InternalMove(
#     _from: CellName,
#     _to: CellName,
#     _promotion: PieceType,
#     _captured: Piece,
#     _piece: Piece,
#     _moveType: MoveType
# )
# class MoveType(str,Enum):
#     NORMAL = 'n' # di chuyển bình thường
#     CAPTURE = 'c' # ăn quân
#     BIG_PAWN = 'b' # tốt di chuyển 2 ô
#     EP_CAPTURE = 'e' # bắt quân qua đường
#     PROMOTION = 'p' # phong cấp eg: tốt phong cấp thành hậu
#     KSIDE_CASTLE = 'k' # nhập thành vua
#     QSIDE_CASTLE = 'q' # nhập thành tướng
#     CP = 'cp' # bắt quân qua đường


class PawnStrategy(PieceStrategy):
    def get_moves(self, game: Chess, from_2d:tuple[int,int]) -> list[InternalMove]:
        board = game._board
        fromX, fromY = from_2d
        piece = board[fromX][fromY]
        moves = []
        direction = -1 if piece.pieceColor == PieceColor.WHITE else 1
        # // di chuyển lên 1 ô
        if board[fromX][fromY + direction].pieceType == PieceType.EMPTY:
            moves.append(InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX, fromY + direction), PieceType.QUEEN, Piece(), piece, MoveType.PROMOTION if self.is_promotion((fromX,fromY + direction),piece.pieceColor) else MoveType.NORMAL))
            # // di chuyển lên 2 ô
            if (fromY == 6 and piece.pieceColor == PieceColor.WHITE) or (fromY == 1 and piece.pieceColor == PieceColor.BLACK):
                if board[fromX][fromY + 2 * direction].pieceType == PieceType.EMPTY:
                    moves.append(InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX, fromY + 2 * direction), PieceType.QUEEN, Piece(), piece, MoveType.BIG_PAWN))
        # // ăn quân
        if fromX > 0 and board[fromX - 1][fromY + direction].pieceColor != piece.pieceColor and board[fromX - 1][fromY + direction].pieceType != PieceType.EMPTY:
            moves.append(InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX - 1, fromY + direction), PieceType.QUEEN, board[fromX - 1][fromY + direction], piece, MoveType.CAPTURE_AND_PROMOTION if self.is_promotion((fromX - 1,fromY + direction),piece.pieceColor) else MoveType.CAPTURE))
        if fromX < 7 and board[fromX + 1][fromY + direction].pieceColor != piece.pieceColor and board[fromX + 1][fromY + direction].pieceType != PieceType.EMPTY:
            moves.append(InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX + 1, fromY + direction), PieceType.QUEEN, board[fromX + 1][fromY + direction], piece, MoveType.CAPTURE_AND_PROMOTION if self.is_promotion((fromX + 1,fromY + direction),piece.pieceColor) else MoveType.CAPTURE))
        return moves
    def is_promotion(self, to_2d:tuple[int,int],color:PieceColor) -> bool:
        if color == PieceColor.WHITE:
            return to_2d[1] == 7
        else:
            return to_2d[1] == 0
        


    def check_move(self,  game: Chess, from_2d:tuple[int,int], to_2d:tuple[int,int]) -> InternalMove:
        pass