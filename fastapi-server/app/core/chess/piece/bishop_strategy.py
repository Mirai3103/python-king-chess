
from .picece_strategy import PieceStrategy
from ..type import CellName, IChess, InternalMove, MoveType, Piece, PieceType
from typing import Optional, List

class BishopStrategy(PieceStrategy):
    def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> List[InternalMove]:
        board = game._board
        from_x, from_y = from_2d
        piece = board[from_x][from_y]
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            for i in range(1, 8):
                to_x, to_y = from_x + i * dx, from_y + i * dy
                if not (0 <= to_x < 8 and 0 <= to_y < 8):
                    break  # Vượt ra khỏi bàn cờ
                if game.get_piece_color(CellName.from_2d(to_x, to_y)) == piece.pieceColor:
                    break  # Gặp quân cờ cùng màu
                move_type = MoveType.NORMAL
                if game.get_piece_type(CellName.from_2d(to_x, to_y)) != PieceType.EMPTY:
                    move_type = MoveType.CAPTURE
                    break  # Gặp quân cờ đối phương, không thể đi tiếp
                
                move =InternalMove(CellName.from_2d(from_x, from_y), CellName.from_2d(to_x, to_y), PieceType.BISHOP, Piece(), piece, move_type)
                if not game.simulate_move(move).is_check(piece.pieceColor):
                    moves.append(move)
        return moves

    def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        from_x, from_y = from_2d
        to_x, to_y = to_2d
        piece = game._board[from_x][from_y]
        color = piece.pieceColor
        dx = to_x - from_x
        dy = to_y - from_y

        # Kiểm tra theo đường chéo
        if abs(dx) == abs(dy):
            direction_x = dx // abs(dx)
            direction_y = dy // abs(dy)
            for i in range(1, abs(dx)):
                check_x, check_y = from_x + i * direction_x, from_y + i * direction_y
                if game._board[check_x][check_y].pieceType != PieceType.EMPTY:
                    return None  # Có quân cờ nằm trên đường đi
            if game._board[to_x][to_y].pieceColor == color:
                return None  # Ô đích có quân cùng màu
            move_type = MoveType.CAPTURE if game._board[to_x][to_y].pieceType != PieceType.EMPTY else MoveType.NORMAL
            return InternalMove(CellName.from_2d(from_x, from_y), CellName.from_2d(to_x, to_y), PieceType.BISHOP, Piece(), piece, move_type)

        return None  # Không di chuyển theo đường chéo
