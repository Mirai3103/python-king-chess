import math
import random
import unittest


from app.core.chess.piece.knight_strategy import KnightStrategy
from app.core.chess.chess import Chess
from app.core.chess.type import CellName,  MoveType, Piece, PieceColor, PieceType
    
import json


def readTestcaseData():

    data = []
    with open('test/knight-move.json') as f:
        data = json.load(f)
        print(f'Loaded {len(data)} testcases.')
    return data

class TestKnightMove(unittest.TestCase):

    def test_same_len(self):
        chess = Chess()
        data = readTestcaseData()
        strategy = KnightStrategy()
        for testcase in data:
            startFen = testcase['startFen']
            chess.load(startFen)
            moves = testcase['moves']
            cell = CellName(testcase['cell'])
            validMoves = strategy.get_moves(chess, CellName.to_2d(cell))
            assert len(validMoves) == len(moves)
    def test_same_move(self):
        chess = Chess()
        data = readTestcaseData()
        strategy = KnightStrategy()
        for testcase in data:
            startFen = testcase['startFen']
            chess.load(startFen)
            moves = testcase['moves']
            cell = CellName(testcase['cell'])
            validMoves = strategy.get_moves(chess, CellName.to_2d(cell))
            for i in range(len(validMoves)):
                exist = False
                for move in moves:
                    if validMoves[i]._from == CellName(move['from']) and validMoves[i]._to == CellName(move['to']) and validMoves[i]._moveType == MoveType(move['type']):
                        exist = True
                        break
                assert exist
    def test_valid_move(seft):
        chess = Chess()
        data = readTestcaseData()
        strategy = KnightStrategy()
        for testcase in data:
            startFen = testcase['startFen']
            chess.load(startFen)
            moves = testcase['moves']
            cell = CellName(testcase['cell'])
            if(len(moves) == 0):
                continue
            randomed_move = moves[math.floor(random.random() * len(moves))]
            move = strategy.check_move(chess, CellName.to_2d(cell), CellName.to_2d(randomed_move['to']))
            seft.assertIsNotNone(move)
            seft.assertEqual(move._from, CellName(randomed_move['from']))
            seft.assertEqual(move._to, CellName(randomed_move['to']))
            seft.assertEqual(move._moveType, MoveType(randomed_move['type']))
    def test_invalid_move(seft):
        chess = Chess()
        strategy = KnightStrategy()
        chess.load('4rk2/p1qb1p2/2p1p1r1/2P1P1Q1/pP4P1/b1P2PKN/R1B3P1/5NR1 b - - 1 29')
        cell = CellName('a7')
        move = strategy.check_move(chess, CellName.to_2d(cell), CellName.to_2d('c7'))
        seft.assertIsNone(move)
        move = strategy.check_move(chess, CellName.to_2d(cell), CellName.to_2d('a2'))
        seft.assertIsNone(move)
        chess.load('rnbqkbnr/ppppp1pp/8/5p2/5P2/8/PPPPP1PP/RNBQKBNR w KQkq - 0 1')
        cell = CellName('f4')
        move = strategy.check_move(chess, CellName.to_2d(cell), CellName.to_2d('f5'))
        print(move)
        seft.assertIsNone(move)

    
if __name__ == '__main__':
    unittest.main()
        