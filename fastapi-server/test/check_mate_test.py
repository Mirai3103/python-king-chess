import unittest

from app.core.chess.chess import Chess
from app.core.chess.type import CellName, InternalMove, MoveType, Piece, PieceColor, PieceType
    
import json


class CheckTest(unittest.TestCase):
    def test1(self):
        #  kiểm tra tốt trắng có thể ăn vua đen
        chess = Chess("rnbqkbnr/pp2pPpp/8/2p5/3p4/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        chess = Chess("rnbqkbnr/pp1Ppppp/8/8/8/2p5/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        # kiểm tra tốt đen có thể ăn vua trắng
        chess = Chess("rnbqkb1r/pp2pppp/5n2/8/2PP4/2N5/PP1p1PPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
        chess = Chess("rnbqkb1r/pp2pppp/5n2/8/2PP4/2N5/PP3pPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
    def test2(self):
        chess = Chess()
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        chess = Chess("rnb1kb1r/ppp1qppp/4pn2/3p2B1/3P4/2N5/PPP2PPP/R2QKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
    def test3(self):
        # kiểm tra quân mã chiếu vua đen
        chess = Chess("r1bqkbnr/pp1npppp/2p2N2/8/3P4/8/PPP2PPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)  
        chess = Chess("r1bqkbnr/pp1npppp/2pN4/8/3P4/8/PPP2PPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        chess = Chess("r1bq1bnr/pp1npppp/2pN4/8/3Pk3/8/PPP1KPPP/R1BQ1BNR w HAha - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
        chess = Chess("r1bq1bnr/pp1npppp/2pN4/8/2kP4/8/PPP1KPPP/R1BQ1BNR w HAha - 0 1")
        self.assertEqual(chess.is_check(PieceColor.BLACK), True)
        self.assertEqual(chess.is_check(PieceColor.WHITE), False)
    
    def test_hau(self):
        # "rnb1kb1r/ppp2ppp/4pn2/3p2B1/3Pq3/2N5/PPP2PPP/R2QKBNR w KQkq - 0 1"
        # "rnb1kb1r/ppp2ppp/4pn2/q2N2B1/3P4/8/PPP2PPP/R2QKBNR w KQkq - 0 1"
        # "rnb1kb1r/ppp2ppp/4pn2/3N1PB1/7q/8/PPP3PP/R2QKBNR w KQkq - 0 1"
        # "rnb1kb1r/ppp2ppp/4pn2/3N1PB1/8/6PP/PPP1K2q/R2Q1BNR w kq - 0 1"

        chess = Chess("rnb1kb1r/ppp2ppp/4pn2/3p2B1/3Pq3/2N5/PPP2PPP/R2QKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        chess = Chess("rnb1kb1r/ppp2ppp/4pn2/q2N2B1/3P4/8/PPP2PPP/R2QKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        chess = Chess("rnb1kb1r/ppp2ppp/4pn2/3N1PB1/7q/8/PPP3PP/R2QKBNR w KQkq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
        chess = Chess("rnb1kb1r/ppp2ppp/4pn2/3N1PB1/8/6PP/PPP1K2q/R2Q1BNR w kq - 0 1")
        self.assertEqual(chess.is_check(PieceColor.WHITE), True)
        self.assertEqual(chess.is_check(PieceColor.BLACK), False)
    

        


if __name__ == '__main__':
    unittest.main()