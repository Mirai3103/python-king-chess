# white is upper case, black is lower case

from .type import DEFAULT_FEN_POSITION, Board, CellName, IChess, InternalMove, MoveType, Piece, PieceColor, PieceType
from typing import Dict
from app.core.chess.piece import PIECES_STRATEGY


class Chess(IChess):
    _board: Board = [[Piece() for _ in range(8)] for _ in range(8)]
    _turn: PieceColor = PieceColor.WHITE
    _history: list[InternalMove] = []
    _castling: Dict[PieceColor, Dict[str, bool]] = {
        PieceColor.WHITE: {'K': True, 'Q': True},
        PieceColor.BLACK: {'k': True, 'q': True}
    }
    _move_number: int = 0
    _ep_square: tuple[int, int] = None
    _half_moves: int = 0

    def is_check(self, color: PieceColor) -> bool:
        # // kiểm tra vua có bị chiếu không
        #Test
        king_position = None
        for x in range(8):
            for y in range(8):
                if self._board[x][y].pieceType == PieceType.KING and self._board[x][y].pieceColor == color:
                   king_position = (x, y)
                   break
            if king_position:
                   break

        # Kiểm tra xem quân vua có bị tấn công không
        if king_position:
            for x in range(8):
                for y in range(8):
                   if self._board[x][y].pieceColor != color and self._is_attacked(x, y, color):
                       return True
        #Test
        return False
    def simulate_move(self, move: InternalMove) -> 'Chess':
        # cloned = Chess(self.fen())
        # cloned._move(move)
        # return cloned
        cloned = Chess(self.fen())
        cloned._move(move)

        # Kiểm tra xem quân vua của mình có bị chiếu không
        if cloned.is_check(cloned._turn):
           print("King is in check after the move.")

        # Lấy vị trí của quân vua địch
        enemy_king_position = None
        for x in range(8):
            for y in range(8):
                if cloned._board[x][y].pieceType == PieceType.KING and cloned._board[x][y].pieceColor != cloned._turn:
                   enemy_king_position = (x, y)
                   break
            if enemy_king_position:
                break

    # Kiểm tra xem quân vua địch có bị chiếu không
        if enemy_king_position and cloned._is_attacked(enemy_king_position[0], enemy_king_position[1], cloned._turn.swap()):
            print("Enemy king is in check after the move.")

        return cloned
        
    
    # def _is_attacked(self, x: int, y: int, color: PieceColor) -> bool:
    #     # xem quân cờ ở vị trí x, y có bị tấn công không
    #     return False
    #
    def _is_attacked(self, x: int, y: int, color: PieceColor) -> bool:
    # Duyệt qua tất cả các ô trên bàn cờ
        # for i in range(8):
        #     for j in range(8):
        #     # Lấy quân cờ tại vị trí (i, j)
        #         piece = self._board[i][j]
        #     # Kiểm tra xem quân cờ này có phải là của đối phương và có thể tấn công ô (x, y) không
        #         if piece.pieceColor != color and self._can_piece_attack(piece, (i, j), (x, y)):
        #            return True
        return False
    def get_piece_color(self, cell: CellName) -> PieceColor:
        x, y = CellName.to_2d(cell)
        return self._board[x][y].pieceColor
    def get_piece_type(self, cell: CellName) -> PieceType:
        x, y = CellName.to_2d(cell)
        return self._board[x][y].pieceType
    
    def _can_piece_attack(self, piece: Piece, piece_position: tuple[int, int], target_position: tuple[int, int]) -> bool:
    # Lấy tất cả các nước đi có thể của quân cờ
        if piece.pieceType == PieceType.EMPTY:
            return False
        if piece_position[0] < 0 or piece_position[0] > 7 or piece_position[1] < 0 or piece_position[1] > 7:
            return False
        if target_position[0] < 0 or target_position[0] > 7 or target_position[1] < 0 or target_position[1] > 7:
            return False
        moves = PIECES_STRATEGY[piece.pieceType].get_moves(self, piece_position)
    # Kiểm tra xem có nước đi nào đến vị trí mục tiêu không
        for move in moves:
            if move._to == CellName.from_2d(target_position[0], target_position[1]):
               return True
        return False
    #
    def __init__(self, fen: str = DEFAULT_FEN_POSITION):
        self.load(fen)

    def load(self, fen: str):
        arr = fen.split(' ')
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        self._turn = PieceColor.WHITE if arr[1] == 'w' else PieceColor.BLACK
        self._castling = {
            PieceColor.WHITE: {'K': 'K' in arr[2], 'Q': 'Q' in arr[2]},
            PieceColor.BLACK: {'k': 'k' in arr[2], 'q': 'q' in arr[2]}
        }
        self._move_number = int(arr[-1])
        self._history = []
        self._half_moves = int(arr[-2])
        if arr[3] != '-':
            self._ep_square = CellName.to_2d(arr[3])
        else:
            self._ep_square = None

        self._board = [[Piece() for _ in range(8)] for _ in range(8)]
        x = 0
        y = 0
        for c in arr[0]:
            if c == '/':
                x = 0
                y += 1
            elif c.isdigit():
                x += int(c)
            else:
                self._board[x][y] = Piece.from_str(c)
                x += 1

    def __str__(self):
        return '\n'.join([' '.join([str(self._board[x][y]) for x in range(8)]) for y in range(8)])

    def _move(self, move: InternalMove):
        us = self._turn
        them = self._turn.swap()
        fromX, fromY = CellName.to_2d(move._from)
        toX, toY = CellName.to_2d(move._to)

        def capture():
            self._board[fromX + (1 if us == PieceColor.WHITE else -1)][fromY] = Piece()

        if move._moveType == MoveType.EP_CAPTURE:
            capture()
        # // di chuyển quân cờ
        self._board[toX][toY] = self._board[fromX][fromY]

        # // nếu phong cấp, thay đổi quân cờ
        if move._moveType == MoveType.PROMOTION:
            self._board[toX][toY] = Piece(move._promotion, us)
        if move._moveType == MoveType.CAPTURE_AND_PROMOTION:
            self._board[toX][toY] = Piece(move._promotion, us)
            capture()
        # // nếu ta di chuyển quân vua, tắt quyền nhập thành
        key_castling_us_k = 'K' if us == PieceColor.WHITE else 'k'
        key_castling_us_q = 'Q' if us == PieceColor.WHITE else 'q'
        key_castling_them_k = 'k' if them == PieceColor.WHITE else 'K'
        key_castling_them_q = 'q' if them == PieceColor.WHITE else 'Q'

        if self._board[toX][toY].pieceType == PieceType.KING:

            self._castling[us] = {key_castling_us_k: False, key_castling_us_q: False}
            if move._moveType == MoveType.KSIDE_CASTLE:
                self._board[toX - 1][toY] = self._board[toX + 1][toY]
                self._board[toX + 1][toY] = Piece()
            elif move._moveType == MoveType.QSIDE_CASTLE:
                self._board[toX + 1][toY] = self._board[toX - 2][toY]
                self._board[toX - 2][toY] = Piece()
        # // tắt quyền nhập thành nếu ta di chuyển quân xe

        if self._board[fromX][fromY].pieceType == PieceType.ROOK:
            if fromX == 0 and fromY == 0:
                self._castling[us][key_castling_us_q] = False
            elif fromX == 7 and fromY == 0:
                self._castling[us][key_castling_us_k] = False
            elif fromX == 0 and fromY == 7:
                self._castling[us][key_castling_us_q] = False
            elif fromX == 7 and fromY == 7:
                self._castling[us][key_castling_us_k] = False

        # // tắt quyền nhập thành nếu ta ăn quân xe
        if self._board[toX][toY].pieceType == PieceType.ROOK:
            if toX == 0 and toY == 0:
                self._castling[them][key_castling_them_q] = False
            elif toX == 7 and toY == 0:
                self._castling[them][key_castling_them_k] = False
        #  // cập nhật vị trí quân tốt nếu tốt di chuyển 2 ô
        if move._moveType == MoveType.BIG_PAWN:
            if us == PieceColor.WHITE:
                self._ep_square = [toX, toY - 1]
            else:
                self._ep_square = [toX, toY + 1]
        else:
            self._ep_square = None
        #  xoá quân cờ ở vị trí cũ
        self._board[fromX][fromY] = Piece()
        # // cập nhật lịch sử
        if move._piece.pieceType == PieceType.PAWN:
            self._half_moves = 0
        elif move._moveType == MoveType.CAPTURE:
            self._half_moves = 0
        else:
            self._half_moves += 1

        if us == PieceColor.BLACK:
            self._move_number += 1

        self._turn = them
        self._history.append(move)

    def fen(self) -> str:
        res = ''
        for y in range(8):
            empty = 0
            for x in range(8):
                p = self._board[x][y]
                if p.pieceType == PieceType.EMPTY:
                    empty += 1
                else:
                    if empty > 0:
                        res += str(empty)
                        empty = 0
                    res += str(p)
            if empty > 0:
                res += str(empty)
            if y < 7:
                res += '/'
        res += ' '
        res += 'w' if self._turn == PieceColor.WHITE else 'b'
        res += ' '
        castling = ''
        if self._castling[PieceColor.WHITE]['K']:
            castling += 'K'
        if self._castling[PieceColor.WHITE]['Q']:
            castling += 'Q'
        if self._castling[PieceColor.BLACK]['k']:
            castling += 'k'
        if self._castling[PieceColor.BLACK]['q']:
            castling += 'q'
        res += castling if castling else '-'
        res += ' '
        res += '-'  # if self._ep_square is None else CellName.from_1d(self._ep_square)
        res += ' '
        res += str(self._half_moves)
        res += ' '
        res += str(self._move_number)
        return res

    def moves(self, from_cell: CellName) -> list[InternalMove]:
        x, y = CellName.to_2d(from_cell)
        strategy = PIECES_STRATEGY[(self._board[x][y].pieceType)]
        return strategy.get_moves(self, CellName.to_2d(from_cell))

    def move(self, from_cell: CellName, to_cell: CellName) -> InternalMove:
        x, y = CellName.to_2d(from_cell)
        strategy = PIECES_STRATEGY[(self._board[x][y].pieceType)]
        move = strategy.check_move(self, CellName.to_2d(from_cell), CellName.to_2d(to_cell))
        if move is not None:
            self._move(move)
        return move

    def undo(self):
        self._history.pop()
        self.re_build()

    def re_build(self):
        self.load(DEFAULT_FEN_POSITION)
        for move in self._history:
            self._move(move)
