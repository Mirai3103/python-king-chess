from typing import Optional

from app.core.chess.chess import Chess

from .picece_strategy import PieceStrategy


from ..type import  CellName, InternalMove, MoveType, Piece, PieceType

class QueenStrategy(PieceStrategy):
    def get_moves(self, game: Chess, from_2d: tuple[int, int]) -> list[InternalMove]:
        board = game._board
        fromX, fromY = from_2d
        piece = board[fromX][fromY]
        moves = []

        # Duyệt theo 8 hướng
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dx, dy in directions:
            x, y = fromX, fromY
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break

                if board[x][y].pieceType == PieceType.EMPTY:
                    move = InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(x, y), PieceType.QUEEN, Piece(), piece, MoveType.NORMAL)
                    if not game.simulate_move(move).is_check(piece.pieceColor):
                        moves.append(move)
                else:
                    if board[x][y].pieceColor != piece.pieceColor:
                        move = InternalMove(CellName.from_2d(fromX, fromY), CellName.from_2d(x, y), PieceType.QUEEN, board[x][y], piece, MoveType.CAPTURE)
                        if not game.simulate_move(move).is_check(piece.pieceColor):
                            moves.append(move)
                    break
        return moves

    def check_move(self, game: Chess, from_2d: tuple[int, int], to_2d: tuple[int, int]) -> Optional[InternalMove]:
        valid_moves = self.get_moves(game, from_2d)
        for move in valid_moves:
            if move._to == CellName.from_2d(*to_2d):
                return move
        return None
