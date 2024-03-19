

from typing import Optional
from ..type import CellName, IChess, InternalMove, MoveType, PieceType
from .picece_strategy import PieceStrategy

class KnightStrategy(PieceStrategy):
    def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> list[InternalMove]:
        board = game._board
        fromX, fromY = from_2d
        piece = board[fromX][fromY]
        moves = []
        # Các hướng di chuyển của quân mã
        directions = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        for dx, dy in directions:
            toX, toY = fromX + dx, fromY + dy

            # Kiểm tra xem ô đích có nằm trong bàn cờ và không phải là quân cờ cùng màu
            if 0 <= toX < 8 and 0 <= toY < 8 and (board[toX][toY].pieceType == PieceType.EMPTY or board[toX][toY].pieceColor != piece.pieceColor):
                captured_piece = board[toX][toY]
                move_type = MoveType.CAPTURE if captured_piece.pieceType != PieceType.EMPTY else MoveType.NORMAL

                move = InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(toX, toY), PieceType.KNIGHT, captured_piece, piece, move_type)

                # Kiểm tra xem nước đi có gây ra tình trạng "chiếu tướng" hay không
                if not game.simulate_move(move).is_check(piece.pieceColor):
                    moves.append(move)

        return moves

    def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        valid_moves = self.get_moves(game, from_2d)
        for move in valid_moves:
            if move._to == CellName.from_2d(*to_2d):
                return move
        return None