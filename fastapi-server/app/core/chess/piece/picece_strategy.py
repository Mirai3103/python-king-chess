from abc import abstractmethod


from ..type import Board,  InternalMove
from ..chess import Chess


class PieceStrategy():
    @abstractmethod
    def get_moves(self, game: Chess, from_2d:tuple[int,int]) -> list[InternalMove]:
        pass
    @abstractmethod
    def check_move(self, game: Chess, from_2d:tuple[int,int], to_2d:tuple[int,int]) -> InternalMove:
        pass

