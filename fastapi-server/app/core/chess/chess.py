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

        self._board[move._to] = self._board[move._from]
        #  xoá quân cờ ở vị trí cũ
        self._board[move._from] = Piece()
        #   // nếu ăn quân , xóa quân cờ
        if move._moveType == MoveType.EP_CAPTURE:
            self._board[move._to + (1 if us == PieceColor.BLACK else -1) * 8] = Piece()
        # // nếu phong cấp, thay đổi quân cờ
        if move._moveType == MoveType.PROMOTION:
            self._board[move._to] = Piece(move._promotion, us)
        # // nếu ta di chuyển quân vua, tắt quyền nhập thành

        if self._board[move._to].pieceType == PieceType.KING:
            key1 = 'K' if us == PieceColor.WHITE else 'k'
            key2 = 'Q' if us == PieceColor.WHITE else 'q'
            self._castling[us] = {key1: False, key2: False}
            if move._moveType == MoveType.KSIDE_CASTLE:
                self._board[move._to - 1] = self._board[move._to + 1]
                self._board[move._to + 1] = Piece()
            elif move._moveType == MoveType.QSIDE_CASTLE:
                self._board[move._to + 1] = self._board[move._to - 2]
                self._board[move._to - 2] = Piece()
        # // tắt quyền nhập thành nếu ta di chuyển quân xe
        if self._board[move._to].pieceType == PieceType.ROOK:
            if move._from == 0:
                self._castling[us]['Q'] = False
            elif move._from == 7:
                self._castling[us]['K'] = False
        # // tắt quyền nhập thành nếu ta ăn quân xe
        if self._board[move._to].pieceType == PieceType.ROOK:
            if move._to == 0:
                self._castling[them]['Q'] = False
            elif move._to == 7:
                self._castling[them]['K'] = False
        #  // cập nhật vị trí quân tốt nếu tốt di chuyển 2 ô
        if move._moveType == MoveType.BIG_PAWN:
            if us == PieceColor.WHITE:
                self._ep_square = move._to - 8
            else:
                self._ep_square = move._to + 8
        else:
            self._ep_square = None
        
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
        self._history.append(MoveEvent(move._moveType, self._board[move._to], move._from, move._to))
        
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
    chess = Chess()
    '''
file moves.txt
{"from":"g1","to":"h3","piece":"n","capturedColor":"b","type":"n","color":"w"}
{"from":"b8","to":"c6","piece":"n","capturedColor":"w","type":"n","color":"b"}
{"from":"h3","to":"g1","piece":"n","capturedColor":"b","type":"n","color":"w"}
{"from":"f7","to":"f5","piece":"p","capturedColor":"w","type":"b","color":"b"}
{"from":"b1","to":"c3","piece":"n","capturedColor":"b","type":"n","color":"w"}
{"from":"f5","to":"f4","piece":"p","capturedColor":"w","type":"n","color":"b"}
    '''
#  fs.appendFileSync('moves.txt', JSON.stringify({
#     from: moveObj.from,
#     to: moveObj.to,
#     promotion: moveObj.promotion,
#     piece: moveObj.piece,
#     captured: moveObj.captured,
#     capturedColor: moveObj.color === 'w' ? 'b' : 'w',
#     type: moveObj.flags,
#     color: moveObj.color
#  }) + '\n')
    # read moves from file
    moves =[]
    f1 = open('fen2.txt', 'a')
    f1.write(chess.fen() + '\n')
    with open('moves.txt', 'r') as f:
        for line in f:
            raw = json.loads(line)
            from_cell = CellName.to_1d(raw['from'])
            to_cell = CellName.to_1d(raw['to'])
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
    
            
