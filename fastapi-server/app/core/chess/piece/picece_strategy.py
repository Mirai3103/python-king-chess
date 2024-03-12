from abc import abstractmethod
from typing import Optional


from ..type import  InternalMove


class PieceStrategy():
    @abstractmethod
    def get_moves(self, game, from_2d:tuple[int,int]) -> list[InternalMove]:
        pass
    @abstractmethod
    def check_move(self, game, from_2d:tuple[int,int], to_2d:tuple[int,int]) -> Optional[InternalMove]:
        pass

