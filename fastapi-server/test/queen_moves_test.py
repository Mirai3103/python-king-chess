import math
import random
import unittest


from app.core.chess.piece.queen_strategy import QueenStrategy
from app.core.chess.chess import Chess
from app.core.chess.type import CellName,  MoveType
    
import json


def readTestcaseData():

    data = []
    with open('test/queen-move.json') as f:
        data = json.load(f)
        print(f'Loaded {len(data)} testcases.')
    return data

class TestQueenMove(unittest.TestCase):

    def test_same_len(self):
        chess = Chess()
        data = readTestcaseData()
        strategy = QueenStrategy()
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
        strategy = QueenStrategy()
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
        strategy = QueenStrategy()
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


    
if __name__ == '__main__':
    unittest.main()
        