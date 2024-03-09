import unittest


from app.core.chess.piece.pawn_strategy import PawnStrategy
from app.core.chess.chess import Chess
from app.core.chess.type import CellName, InternalMove, MoveType, Piece, PieceColor, PieceType
    
import json


def readTestcaseData():

    data = []
    with open('test/pawn-move.json') as f:
        data = json.load(f)
    return data

class TestPawnMove(unittest.TestCase):
#     {
#     "startFen": "4b1k1/5rq1/2p1pP2/2PQ3N/p1r5/2P2P1N/p5PK/b2R4 b - - 4 52",
#     "cell": "c6",
#     "moves": [
#       {
#         "from": "c6",
#         "to": "d5",
#         "piece": "p",
#         "captured": "q",
#         "capturedColor": "w",
#         "type": "c",
#         "color": "b"
#       }
#     ]
#   },
    def test_same_len(self):
        chess = Chess()
        data = readTestcaseData()
        strategy = PawnStrategy()
        for testcase in data:
            startFen = testcase['startFen']
            chess.load(startFen)
            moves = testcase['moves']
            cell = CellName(testcase['cell'])
            validMoves = strategy.get_moves(chess._board, CellName.to_2d(cell))
            assert len(validMoves) == len(moves)
    def test_same_move(self):
        chess = Chess()
        data = readTestcaseData()
        strategy = PawnStrategy()
        for testcase in data:
            startFen = testcase['startFen']
            chess.load(startFen)
            moves = testcase['moves']
            cell = CellName(testcase['cell'])
            validMoves = strategy.get_moves(chess._board, CellName.to_2d(cell))
            for i in range(len(validMoves)):
                exist = False
                for move in moves:
                    if validMoves[i]._from == CellName(move['from']) and validMoves[i]._to == CellName(move['to']) and validMoves[i]._moveType == MoveType(move['type']):
                        exist = True
                        print(f'{validMoves[i]._from} -> {validMoves[i]._to} , {validMoves[i]._moveType} , {validMoves[i]._piece}')
                        print(f'{CellName(move["from"])} -> {CellName(move["to"])} , {MoveType(move["type"])} , {Piece(PieceType(move["piece"]), PieceColor(move["color"]))}')
                        print('-------------------')
                        break
                assert exist
                
            
                
                

if __name__ == '__main__':
    unittest.main()
        