from abc import abstractmethod


from ..type import Board,  InternalMove



class PieceStrategy():
    @abstractmethod
    def get_moves(self, board: Board, from_2d:tuple[int,int]) -> list[InternalMove]:
        pass
    @abstractmethod
    def check_move(self, board: Board, from_2d:tuple[int,int], to_2d:tuple[int,int]) -> InternalMove:
        pass

