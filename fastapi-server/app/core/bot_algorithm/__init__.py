

from abc import abstractmethod
from enum import Enum
import os

from stockfish import Stockfish    

from app.core.chess.chess import Chess
from app.core.chess.type import CellName, IChess, InternalMove, MoveType, PieceColor,PieceType


class Dificulty(int,Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class BotAlgorithmStrategy():
    @abstractmethod
    def get_best_move(self,color:PieceColor,chess:IChess) -> str:
        pass


class RandomBot(BotAlgorithmStrategy):
    def get_best_move(self,color:PieceColor,chess:IChess) -> str:
        import random
        moves = chess.moves_of_color(color)
        move = random.choice(moves)
        chess.move(move._from, move._to)
        return chess.fen()
    
PIECE_VALUES = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 100
}


class GreedyBot(BotAlgorithmStrategy):
    def get_best_move(self,color:PieceColor,chess:IChess) ->  str:
        moves = chess.moves_of_color(color)
        best_move = None
        best_value = -100000
        for move in moves:
            value = 0
            if move._moveType== MoveType.CAPTURE:
                value += PIECE_VALUES[chess.getPiece(move._to).pieceType]
            if move._moveType== MoveType.PROMOTION:
                value += PIECE_VALUES[PieceType.QUEEN]
            else:
                cloned = chess.simulate_move(move)
                opponent_color = color.swap()
                for square in cloned.squares_of_color(color):
                    x,y = CellName.to_2d(square)
                    if cloned.is_attacked(x,y, color):
                        value -= PIECE_VALUES[cloned.getPiece(square).pieceType]
                for square in cloned.squares_of_color(opponent_color):
                    if cloned.is_attacked(x,y, opponent_color):
                        value += PIECE_VALUES[cloned.getPiece(square).pieceType]
            if value > best_value:
                best_value = value
                best_move = move
        chess.move(best_move._from, best_move._to)
        return chess.fen()



class StockfishBot(BotAlgorithmStrategy):
    def get_best_move(self,color:PieceColor,chess:IChess) -> str:
        isWindows = os.name == 'nt'
        if isWindows:
            path = "stockfish/windows/stockfish.exe"
        else:
            path = "stockfish/linux/stockfish"
        st= Stockfish(path=path,
                        depth=10,
                        parameters={
                            "Threads": 1,
                            "Skill Level": 16,
                            "Hash": 64,
                        }
                        )
        st.set_fen_position(chess.fen())
        bot_move = st.get_best_move()
        st.make_moves_from_current_position([ bot_move])
        newFen = st.get_fen_position()
        return newFen
        
    
if __name__ == "__main__":
    chess = Chess("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    bot = RandomBot()
    print(bot.get_best_move(chess._turn,chess))
    
def get_bot(dificulty:Dificulty) -> BotAlgorithmStrategy:
    if dificulty == Dificulty.EASY:
        return RandomBot()
    if dificulty == Dificulty.MEDIUM:
        return GreedyBot()
    if dificulty == Dificulty.HARD:
        return StockfishBot()
    return RandomBot()
    