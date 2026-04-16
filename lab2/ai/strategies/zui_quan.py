from random import randrange

from core.game_utils import BoardType
from core.piece import Piece

from ai.strategies.strategy import Strategy


class ZuiQuan(Strategy):
    """
    Zui Quan (Drunk Fist) strategy: Random decision-making for unpredictable gameplay.
    """

    def rate_position(self, board: BoardType, player: Piece) -> int:
        """
        Returns a random score, making every position equally likely to be evaluated."""
        return randrange(-1000, 1000)
