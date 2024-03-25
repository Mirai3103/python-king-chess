from abc import abstractmethod
from enum import Enum
from typing import Optional

from fastapi.background import P

class PieceType(str,Enum):
    # quân tốt 
    PAWN = 'p' 
    # quân mã
    KNIGHT = 'n'
    # quân tượng
    BISHOP = 'b'
    # quân xe
    ROOK = 'r'
    # quân hậu
    QUEEN = 'q'
    # quân vua
    KING = 'k'
    # ô trống
    EMPTY = '0'

class PieceColor(str,Enum):
    WHITE = 'w'
    BLACK = 'b'
    NONE = 'n'

    def swap(self)->'PieceColor':
        if self == PieceColor.WHITE:
            return PieceColor.BLACK
        elif self == PieceColor.BLACK:
            return PieceColor.WHITE
        else:
            return PieceColor.NONE

class CellName(str,Enum):
    A8 = 'a8'
    B8 = 'b8'
    C8 = 'c8'
    D8 = 'd8'
    E8 = 'e8'
    F8 = 'f8'
    G8 = 'g8'
    H8 = 'h8'
    A7 = 'a7'
    B7 = 'b7'
    C7 = 'c7'
    D7 = 'd7'
    E7 = 'e7'
    F7 = 'f7'
    G7 = 'g7'
    H7 = 'h7'
    A6 = 'a6'
    B6 = 'b6'
    C6 = 'c6'
    D6 = 'd6'
    E6 = 'e6'
    F6 = 'f6'
    G6 = 'g6'
    H6 = 'h6'
    A5 = 'a5'
    B5 = 'b5'
    C5 = 'c5'
    D5 = 'd5'
    E5 = 'e5'
    F5 = 'f5'
    G5 = 'g5'
    H5 = 'h5'
    A4 = 'a4'
    B4 = 'b4'
    C4 = 'c4'
    D4 = 'd4'
    E4 = 'e4'
    F4 = 'f4'
    G4 = 'g4'
    H4 = 'h4'
    A3 = 'a3'
    B3 = 'b3'
    C3 = 'c3'
    D3 = 'd3'
    E3 = 'e3'
    F3 = 'f3'
    G3 = 'g3'
    H3 = 'h3'
    A2 = 'a2'
    B2 = 'b2'
    C2 = 'c2'
    D2 = 'd2'
    E2 = 'e2'
    F2 = 'f2'
    G2 = 'g2'
    H2 = 'h2'
    A1 = 'a1'
    B1 = 'b1'
    C1 = 'c1'
    D1 = 'd1'
    E1 = 'e1'
    F1 = 'f1'
    G1 = 'g1'
    H1 = 'h1'
    @staticmethod
    def from_2d(x:int, y:int)->'CellName':
        return CellName(chr(97 + x) + str(8 - y))
    @staticmethod
    def to_2d(s:str):
        return ord(s[0]) - 97, 8 - int(s[1])
    
    

DEFAULT_FEN_POSITION ='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class Piece:
    pieceType:PieceType
    pieceColor:PieceColor
   
    def __init__(self, pieceType:PieceType= PieceType.EMPTY, pieceColor:PieceColor=PieceColor.NONE):
        self.pieceType = pieceType
        self.pieceColor = pieceColor
    @staticmethod
    def from_str(s:str):
        pieceColor = PieceColor.WHITE if s.isupper() else PieceColor.BLACK
        pieceType = PieceType(s.lower())
        return Piece(pieceType, pieceColor)

    def __str__(self):
        return self.pieceType.value if self.pieceColor == PieceColor.BLACK else self.pieceType.value.upper()
    


class MoveType(str,Enum):
    NORMAL = 'n' # di chuyển bình thường
    CAPTURE = 'c' # ăn quân
    BIG_PAWN = 'b' # tốt di chuyển 2 ô
    EP_CAPTURE = 'e' # bắt quân qua đường
    PROMOTION = 'p' # phong cấp eg: tốt phong cấp thành hậu
    KSIDE_CASTLE = 'k' # nhập thành vua
    QSIDE_CASTLE = 'q' # nhập thành tướng
    CAPTURE_AND_PROMOTION = 'cp' # bắt quân qua đường và phong cấp 


class InternalMove:
    _from:CellName
    _to:CellName
    _promotion:PieceType
    _captured:Piece
    _piece:Piece
    _moveType:MoveType
    
    def __init__(self, _from:CellName, _to:CellName, _promotion:PieceType=Piece(), _captured:Piece=Piece(), _piece:Piece=Piece(), _moveType:MoveType=MoveType.NORMAL):
        
        self._from = _from
        self._to = _to
        self._promotion = _promotion
        self._captured = _captured
        self._piece = _piece
        self._moveType = _moveType

    def __str__(self):
        return f'{self._from} -> {self._to} , {self._moveType} , {self._piece}'

Board = list[list[Piece]]

class IllegalMoveError(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)


class IChess:
    _board:Board
    _turn:PieceColor
    _castling:dict[PieceColor,dict[str,bool]]
    
    @abstractmethod
    def load(self, fen: str):
        pass
    @abstractmethod
    def moves(self, from_cell: CellName) -> list[InternalMove]:
        pass
    @abstractmethod
    def move(self, from_cell: CellName, to_cell: CellName) -> InternalMove:
        pass
    @abstractmethod
    def simulate_move(self, move: InternalMove) -> 'IChess':
        pass
    @abstractmethod
    def is_check(self, color: PieceColor) -> bool:
        pass
    @abstractmethod
    def is_checkmate(self, color: PieceColor) -> bool:
        pass
    @abstractmethod
    def fen(self) -> str:
        pass