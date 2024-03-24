# from typing import Optional


# from .picece_strategy import PieceStrategy


# from ..type import   CellName, IChess, InternalMove, MoveType, Piece, PieceType

# class BishopStrategy(PieceStrategy):
#     def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> list[InternalMove]:
#        moves = []
#        return moves

#     def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
#         return None
from typing import Optional
from .piece_strategy import PieceStrategy
from ..type import CellName, IChess, InternalMove, MoveType, Piece, PieceType
class BishopStrategy(PieceStrategy):
    def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> list[InternalMove]:
        moves = []
        x, y = from_2d
        color = game.get_piece_color(CellName.from_2d(from_2d))
        # Các hướng quân tượng có thể di chuyển
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

        for dx, dy in directions:
            for i in range(1, 8):
                to_x, to_y = x + i * dx, y + i * dy
                if not (0 <= to_x < 8 and 0 <= to_y < 8):
                    break  # Vượt ra khỏi bàn cờ
                if game.get_piece_color(CellName.from_2d((to_x, to_y))) == color:
                    break  # Gặp quân cờ cùng màu
                move_type = MoveType.NORMAL
                if game.get_piece_type(CellName.from_2d((to_x, to_y))) != PieceType.EMPTY:
                    move_type = MoveType.CAPTURE
                    break  # Gặp quân cờ đối phương, không thể đi tiếp
                moves.append(InternalMove(CellName.from_2d((x, y)), CellName.from_2d((to_x, to_y)), move_type))
        return moves

    def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        x, y = from_2d
        to_x, to_y = to_2d
        color = game.get_piece_color(CellName.from_2d(from_2d))
        dx = to_x - x
        dy = to_y - y

        if abs(dx) != abs(dy):
            return None  # Không di chuyển theo đường chéo

        # Kiểm tra các ô trên đường đi
        direction_x = 1 if dx > 0 else -1
        direction_y = 1 if dy > 0 else -1
        for i in range(1, abs(dx)):
            check_x, check_y = x + i * direction_x, y + i * direction_y
            if game.get_piece_type(CellName.from_2d((check_x, check_y))) != PieceType.EMPTY:
                return None  # Có quân cờ nằm trên đường đi

        if game.get_piece_color(CellName.from_2d(to_2d)) == color:
            return None  # Ô đích có quân cùng màu

        # Trả về nước đi hợp lệ
        move_type = MoveType.CAPTURE if game.get_piece_type(CellName.from_2d(to_2d)) != PieceType.EMPTY else MoveType.NORMAL
        return InternalMove(CellName.from_2d(from_2d), CellName.from_2d(to_2d), move_type)