from ai.strategies.strategy import Strategy
from core.game_utils import BoardType
from core.piece import Piece

from ai.heuristics.pieces_heuristics import (
    penalty_for_being_attacked,
    penalty_for_enemies_in_fov,
)
from ai.heuristics.player_heuristics import is_one_move_to_victory, most_advanced_piece


class FastLane(Strategy):
    """
    Fast Lane strategy: Prioritizes rapid piece advancement with tactical awareness.
    """

    WEIGHTS = {
        'victory': 1,
        'attacked': 1,
        'enemies_in_fov': 1,
        'advancement': 15,
    }

    def rate_position(self, board: BoardType, player: Piece) -> int:
        return (
            self.WEIGHTS['victory'] * is_one_move_to_victory(board, player)
            + self.WEIGHTS['attacked'] * penalty_for_being_attacked(board, player)
            + self.WEIGHTS['enemies_in_fov'] * penalty_for_enemies_in_fov(board, player)
            + self.WEIGHTS['advancement'] * most_advanced_piece(board, player)
        )
