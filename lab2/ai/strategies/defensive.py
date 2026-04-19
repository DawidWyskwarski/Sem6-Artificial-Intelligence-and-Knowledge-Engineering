from ai.strategies.strategy import Strategy
from core.game_utils import Board, enemy_color
from core.piece import Piece

from ai.heuristics.pieces_heuristics import (
    count_supporting_each_other,
    penalty_for_being_attacked,
)
from ai.heuristics.player_heuristics import (
    victory_reward,
    piece_difference,
    covered_area,
    most_advanced_piece,
)


class Defensive(Strategy):
    """
    Defensive strategy: Prioritizes piece safety and material advantage.
    """

    WEIGHTS = {
        "victory_reward": 1,
        "defeat_penalty": -1,
        "support": 1,
        "covered_area": 1,
        "attacked": 1,
        "advanced_enemy": -5,
        "piece_difference": 20,
    }

    def rate_position(self, board: Board, player: Piece) -> int:
        return (
            self.WEIGHTS["victory_reward"] * victory_reward(board, player)
            + self.WEIGHTS["defeat_penalty"] * victory_reward(board, enemy_color(player))
            + self.WEIGHTS["support"] * count_supporting_each_other(board, player)
            + self.WEIGHTS["covered_area"] * covered_area(board, player)
            + self.WEIGHTS["attacked"] * penalty_for_being_attacked(board, player)
            + self.WEIGHTS["advanced_enemy"]
            * most_advanced_piece(
                board, Piece.BLACK if player == Piece.WHITE else Piece.WHITE
            )
            + self.WEIGHTS["piece_difference"] * piece_difference(board, player)
        )
