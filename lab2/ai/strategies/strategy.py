from abc import ABC, abstractmethod

from core.game_utils import BoardType
from core.piece import Piece


class Strategy(ABC):

    @abstractmethod
    def rate_position(self, board: BoardType, player: Piece) -> int:
        pass
