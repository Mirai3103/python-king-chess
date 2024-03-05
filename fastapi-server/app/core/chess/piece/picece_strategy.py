from abc import abstractmethod


from ..type import Board,  InternalMove



class PieceStrategy():
    @abstractmethod
    def get_moves(self, board: Board, from_1d: int) -> list[InternalMove]:
        pass
    @abstractmethod
    def check_move(self, board: Board, from_1d: int, to_1d: int) -> InternalMove:
        
        pass

