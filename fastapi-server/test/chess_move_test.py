import unittest

from app.core.chess.chess import Chess
from app.core.chess.type import CellName, InternalMove, MoveType, Piece, PieceColor, PieceType
    
import json

def readTestcaseData():

    data = []
    with open('test/chess.test.json') as f:
        data = json.load(f)
    return data

class TestMoveAndFen(unittest.TestCase):
    def test_move(self):
        chess = Chess()
        data = readTestcaseData()
        for testcase in data:
            move = testcase['move']
            from_cell = CellName(move['from'])
            to_cell = CellName(move['to'])
            piecet = PieceType(move['piece'])
            piece_color = PieceColor(move['color'])
            piece = Piece(piecet, piece_color)
            move_type = MoveType(move['type'])
            piece_captured = PieceType.EMPTY if move.get('captured') is None else PieceType(move['captured'])
            prom = PieceType.EMPTY if move.get('promotion') is None else PieceType(move['promotion'])
            piece_captured_color = PieceColor.BLACK if move['capturedColor'] == 'b' else PieceColor.WHITE
            captured = Piece(piece_captured, piece_captured_color)
            internalMove= InternalMove(from_cell, to_cell,prom,captured,piece,move_type)
            chess._move(internalMove)
            self.assertEqual(chess.fen(), testcase['endFen'])

if __name__ == '__main__':
    unittest.main()