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
from .picece_strategy import PieceStrategy
from ..type import CellName, IChess, InternalMove, MoveType, Piece, PieceType
# class BishopStrategy(PieceStrategy):
#     def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> list[InternalMove]:
#         moves = []
#         x, y = from_2d
#         color = game.get_piece_color(CellName.from_2d(fromX, fromY))
#         # Các hướng quân tượng có thể di chuyển
#         directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  

#         for dx, dy in directions:
#             for i in range(1, 8):
#                 to_x, to_y = x + i * dx, y + i * dy
#                 if not (0 <= to_x < 8 and 0 <= to_y < 8):
#                     break  # Vượt ra khỏi bàn cờ
#                 if game.get_piece_color(CellName.from_2d(to_x, to_y)) == color:
#                     break  # Gặp quân cờ cùng màu
#                 move_type = MoveType.NORMAL
#                 if game.get_piece_type(CellName.from_2d(to_x, to_y)) != PieceType.EMPTY:
#                     move_type = MoveType.CAPTURE
#                     break  # Gặp quân cờ đối phương, không thể đi tiếp
#                 moves.append(InternalMove(CellName.from_2d(x, y), CellName.from_2d(to_x, to_y), move_type))
#         return moves

#     def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
#         x, y = from_2d
#         to_x, to_y = to_2d
#         color = game.get_piece_color(CellName.from_2d(fromX, fromY))
#         dx = to_x - x
#         dy = to_y - y

#         if abs(dx) != abs(dy):
#             return None  # Không di chuyển theo đường chéo

#         # Kiểm tra các ô trên đường đi
#         direction_x = 1 if dx > 0 else -1
#         direction_y = 1 if dy > 0 else -1
#         for i in range(1, abs(dx)):
#             check_x, check_y = x + i * direction_x, y + i * direction_y
#             if game.get_piece_type(CellName.from_2d(check_x, check_y)) != PieceType.EMPTY:
#                 return None  # Có quân cờ nằm trên đường đi

#         if game.get_piece_color(CellName.from_2d(to_2d)) == color:
#             return None  # Ô đích có quân cùng màu

#         # Trả về nước đi hợp lệ
#         move_type = MoveType.CAPTURE if game.get_piece_type(CellName.from_2d(to_2d)) != PieceType.EMPTY else MoveType.NORMAL
#         return InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(to_2d), move_type)
# class BishopStrategy(PieceStrategy):
#     def get_moves(self, game: IChess, from_2d: tuple[int, int]) -> List[InternalMove]:
#         board = game._board
#         from_x, from_y = from_2d
#         piece = board[from_x][from_y]
#         moves = []
#         directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

#         for dx, dy in directions:
#             for i in range(1, 8):
#                 to_x, to_y = from_x + i * dx, from_y + i * dy
#                 if not (0 <= to_x < 8 and 0 <= to_y < 8):
#                     break  # Vượt ra khỏi bàn cờ
#                 if game.get_piece_color(CellName.from_2d(to_x, to_y)) == piece.pieceColor:
#                     break  # Gặp quân cờ cùng màu
#                 move_type = MoveType.NORMAL
#                 if game.get_piece_type(CellName.from_2d(to_x, to_y)) != PieceType.EMPTY:
#                     move_type = MoveType.CAPTURE
#                     break  # Gặp quân cờ đối phương, không thể đi tiếp
#                 moves.append(InternalMove(CellName.from_2d(from_x, from_y), CellName.from_2d(to_x, to_y),PieceType.BISHOP,Piece(),piece, move_type))
#         return moves

#     def check_move(self, game: IChess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
#         valid_moves = self.get_moves(game, from_2d)
#         for move in valid_moves:
#             if move._to == CellName.from_2d(*to_2d):
#                 return move
#         return None
from typing import Optional, List
from .picece_strategy import PieceStrategy
from ..type import CellName, IChess, InternalMove, MoveType, Piece, PieceType

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
