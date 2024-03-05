# white is upper case, black is lower case

from type import DEFAULT_FEN_POSITION, CellName, InternalMove, MoveEvent, MoveType, Piece, PieceColor, PieceType
from typing import Dict


class Chess:
    
    def __init__(self, fen:str=DEFAULT_FEN_POSITION):
        self._board = [Piece() for _ in range(64)]
        self._turn : PieceColor =PieceColor.WHITE
        self._history :MoveEvent = []
        self._castling: Dict[PieceColor, Dict[str, bool]] = {
            PieceColor.WHITE: {'K': True, 'Q': True},
            PieceColor.BLACK: {'k': True, 'q': True}
        }
        self._move_number = 0
        self._ep_square = None
        self._half_moves = 0

        self.load(fen)
    
    def load(self, fen:str):
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
            self._ep_square = CellName.to_1d(arr[3])
        else:
            self._ep_square = None
            
        self._board = [Piece() for _ in range(64)]
        x = 0
        y = 0
        for c in arr[0]:
            if c == '/':
                x = 0
                y += 1
            elif c.isdigit():
                x += int(c)
            else:
                self._board[x + y * 8] = Piece.from_str(c)
                x += 1

    def __str__(self):
        return '\n'.join([' '.join([str(self._board[x + y * 8]) for x in range(8)]) for y in range(8)])
        
    def _move(self, move:InternalMove):
        us = self._turn
        them = self._turn.swap()
        from_1d = CellName.to_1d(move._from)
        to_1d = CellName.to_1d(move._to)
   
        if move._moveType == MoveType.EP_CAPTURE:
            self._board[to_1d + (1 if us == PieceColor.BLACK else -1) * 8] = Piece()
        # // di chuyển quân cờ
        self._board[to_1d] = self._board[from_1d]

     
   
        # // nếu phong cấp, thay đổi quân cờ
        if move._moveType == MoveType.PROMOTION:
            self._board[to_1d] = Piece(move._promotion, us)
        # // nếu ta di chuyển quân vua, tắt quyền nhập thành
        key_castling_us_k = 'K' if us == PieceColor.WHITE else 'k'
        key_castling_us_q = 'Q' if us == PieceColor.WHITE else 'q'
        key_castling_them_k = 'k' if them == PieceColor.WHITE else 'K'
        key_castling_them_q = 'q' if them == PieceColor.WHITE else 'Q'

        if self._board[to_1d].pieceType == PieceType.KING:
      
            self._castling[us] = {key_castling_us_k: False, key_castling_us_q: False}
            if move._moveType == MoveType.KSIDE_CASTLE:
                self._board[to_1d - 1] = self._board[to_1d + 1]
                self._board[to_1d + 1] = Piece()
            elif move._moveType == MoveType.QSIDE_CASTLE:
                self._board[to_1d + 1] = self._board[to_1d - 2]
                self._board[to_1d - 2] = Piece()
        # // tắt quyền nhập thành nếu ta di chuyển quân xe
     
        if self._board[from_1d].pieceType == PieceType.ROOK:
            if from_1d  == 0:
                self._castling[us][key_castling_us_q] = False
            elif from_1d  == 7:
                self._castling[us][key_castling_us_k] = False
            elif from_1d  == 56:
                self._castling[us][key_castling_us_q] = False
            elif from_1d  == 63:
                self._castling[us][key_castling_us_k] = False

        # // tắt quyền nhập thành nếu ta ăn quân xe
        if self._board[to_1d].pieceType == PieceType.ROOK:
            if to_1d == 0:
                self._castling[them][key_castling_them_q] = False
            elif to_1d == 7:
                self._castling[them][key_castling_them_k] = False
        #  // cập nhật vị trí quân tốt nếu tốt di chuyển 2 ô
        if move._moveType == MoveType.BIG_PAWN:
            if us == PieceColor.WHITE:
                self._ep_square = to_1d - 8
            else:
                self._ep_square = to_1d + 8
        else:
            self._ep_square = None
           #  xoá quân cờ ở vị trí cũ
        self._board[from_1d ] = Piece()
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
        self._history.append(MoveEvent(move._moveType, self._board[to_1d], move._from , move._to))
        
    def fen(self)->str:
        res = ''
        for y in range(8):
            empty = 0
            for x in range(8):
                p = self._board[x + y * 8]
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
        res += '-' #if self._ep_square is None else CellName.from_1d(self._ep_square)
        res += ' '
        res += str(self._half_moves)
        res += ' '
        res += str(self._move_number)
        return res
    # // trả về danh sách các nước đi hợp lệ từ ô cờ đang xét
    def moves(self, from_cell:CellName)->list[str]:
  
        pass
    def move(self, from_cell:CellName , to_cell:CellName):
        # // kiểm tra xem nước đi có hợp lệ không
        # // nếu hợp lệ, di chuyển quân cờ và cập nhật lịch sử
        pass
       


        


        
        
    
import json


if __name__ == "__main__":
    # test
    chess = Chess()


    moves =[]
    f1 = open('fen2.txt', 'a')
    f1.write(chess.fen() + '\n')
    with open('moves.txt', 'r') as f:
        for line in f:
            raw = json.loads(line)
            from_cell = CellName(raw['from'])
            to_cell = CellName(raw['to'])
            piecet = PieceType(raw['piece'])
            piece_color = PieceColor(raw['color'])
            piece = Piece(piecet, piece_color)
            move_type = MoveType(raw['type'])
            piece_captured = PieceType.EMPTY if raw.get('captured') is None else PieceType(raw['captured'])
            prom = PieceType.EMPTY if raw.get('promotion') is None else PieceType(raw['promotion'])
            piece_captured_color = PieceColor.BLACK if raw['capturedColor'] == 'b' else PieceColor.WHITE
            captured = Piece(piece_captured, piece_captured_color)
            moves.append(InternalMove(from_cell, to_cell,prom,captured,piece,move_type))
    for move in moves:
        chess._move(move)
    
        f1.write(chess.fen() + '\n')
    f.close()
    
            
