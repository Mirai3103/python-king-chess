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
        
    def move(self, move:InternalMove):
        us = self._turn
        them = self._turn.swap()

        # self._history.append(MoveEvent(move.moveType, self._board[move._from], move._from, move._to))
        self._board[move._to] = self._board[move._from]
        #  remove the piece from the original square
        self._board[move._from] = Piece()
        #   // if ep capture, remove the captured pawn
        if move._moveType == MoveType.EP_CAPTURE:
            self._board[move._to + (1 if us == PieceColor.BLACK else -1) * 8] = Piece()
        # // if pawn promotion, replace with new piece
        if move._moveType == MoveType.PROMOTION:
            self._board[move._to] = Piece(move._promotion, us)
        # // if we moved the king
        if self._board[move._to].pieceType == PieceType.KING:
            self._castling[us] = {'K': False, 'Q': False}
            # // if we castled, move the rook next to the king
            if move._moveType == MoveType.KSIDE_CASTLE:
                self._board[move._to - 1] = self._board[move._to + 1]
                self._board[move._to + 1] = Piece()
            elif move._moveType == MoveType.QSIDE_CASTLE:
                self._board[move._to + 1] = self._board[move._to - 2]
                self._board[move._to - 2] = Piece()
        # // turn off castling if we move a rook
        if self._board[move._to].pieceType == PieceType.ROOK:
            if move._from == 0:
                self._castling[us]['Q'] = False
            elif move._from == 7:
                self._castling[us]['K'] = False
        # // turn off castling if we capture a rook
        if self._board[move._to].pieceType == PieceType.ROOK:
            if move._to == 0:
                self._castling[them]['Q'] = False
            elif move._to == 7:
                self._castling[them]['K'] = False
        #  // if big pawn move, update the en passant square
        if move._moveType == MoveType.BIG_PAWN:
            if us == PieceColor.WHITE:
                self._ep_square = move._to - 8
            else:
                self._ep_square = move._to + 8
        else:
            self._ep_square = None
        
        # // reset the 50 move counter if a pawn is moved or a piece is captured
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
        res += '-' if self._ep_square is None else CellName.to_2d(self._ep_square)
        res += ' '
        res += str(self._half_moves)
        res += ' '
        res += str(self._move_number)
        return res
    
    

        


if __name__ == "__main__":
    chess = Chess()
    print(chess.fen())

    chess.move(InternalMove(CellName.to_1d('e2'), CellName.to_1d('e4'), PieceType.EMPTY, Piece(), Piece(PieceType.PAWN, PieceColor.WHITE), MoveType.NORMAL))
    print(chess.fen())
