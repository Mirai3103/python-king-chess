

from typing import Optional
from ..type import  CellName, IChess, MoveType, Piece,InternalMove,PieceColor, PieceType
from .picece_strategy import PieceStrategy


class PawnStrategy(PieceStrategy):
    def get_moves(self, game: IChess, from_2d:tuple[int,int]) -> list[InternalMove]:
     
        board = game._board
        
        fromX, fromY = from_2d
        piece = board[fromX][fromY]
        moves = []
        direction = -1 if piece.pieceColor == PieceColor.WHITE else 1
        # // di chuyển lên 1 ô
        if board[fromX][fromY + direction].pieceType == PieceType.EMPTY :
            move=InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX, fromY + direction), PieceType.QUEEN, Piece(), piece, MoveType.PROMOTION if self.is_promotion((fromX,fromY + direction),piece.pieceColor) else MoveType.NORMAL)
            if not game.simulate_move(move).is_check(piece.pieceColor)  :
                moves.append(move)
            # // di chuyển lên 2 ô
            if (fromY == 6 and piece.pieceColor == PieceColor.WHITE) or (fromY == 1 and piece.pieceColor == PieceColor.BLACK):
                if board[fromX][fromY + 2 * direction].pieceType == PieceType.EMPTY:
                    move=InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX, fromY + 2 * direction), PieceType.QUEEN, Piece(), piece, MoveType.BIG_PAWN)
                    if not game.simulate_move(move).is_check(piece.pieceColor)  :
                        moves.append(move)
        # // ăn quân
        if fromX > 0 and board[fromX - 1][fromY + direction].pieceColor != piece.pieceColor and board[fromX - 1][fromY + direction].pieceType != PieceType.EMPTY:
            move=InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX - 1, fromY + direction), PieceType.QUEEN, board[fromX - 1][fromY + direction], piece, MoveType.CAPTURE_AND_PROMOTION if self.is_promotion((fromX - 1,fromY + direction),piece.pieceColor) else MoveType.CAPTURE)
            if not game.simulate_move(move).is_check(piece.pieceColor)  :
                moves.append(move)
        if fromX < 7 and board[fromX + 1][fromY + direction].pieceColor != piece.pieceColor and board[fromX + 1][fromY + direction].pieceType != PieceType.EMPTY:
            move=InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(fromX + 1, fromY + direction), PieceType.QUEEN, board[fromX + 1][fromY + direction], piece, MoveType.CAPTURE_AND_PROMOTION if self.is_promotion((fromX + 1,fromY + direction),piece.pieceColor) else MoveType.CAPTURE)
            if not game.simulate_move(move).is_check(piece.pieceColor)  :
                moves.append(move)
        return moves
    def is_promotion(self, to_2d:tuple[int,int],color:PieceColor) -> bool:
        if color == PieceColor.WHITE:
            return to_2d[1] == 0
        else:
            return to_2d[1] == 7
        


    def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        valid_moves = self.get_moves(game, from_2d)
        for move in valid_moves:
            if move._to == CellName.from_2d(*to_2d):
                return move
        return None