from abc import ABC, abstractmethod

from core.game_utils import Board
from core.piece import Piece


class Strategy(ABC):

    @abstractmethod
    def rate_position(self, board: Board, player: Piece) -> int:
        pass
