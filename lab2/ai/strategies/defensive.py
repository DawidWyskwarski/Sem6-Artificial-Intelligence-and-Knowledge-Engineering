from ai.strategies.strategy import Strategy
from core.game_utils import BoardType
from core.piece import Piece

from ai.heuristics.pieces_heuristics import (
    count_supporting_each_other,
    penalty_for_being_attacked,
)
from ai.heuristics.player_heuristics import (
    is_one_move_to_victory,
    piece_difference,
    covered_area,
    most_advanced_piece,
)


class Defensive(Strategy):
    """
    Defensive strategy: Prioritizes piece safety and material advantage.
    """

    WEIGHTS = {
        "victory": 1,
        "support": 1,
        "covered_area": 1,
        "attacked": 1,
        "advanced_enemy": 1,
        "piece_difference": 20,
    }

    def rate_position(self, board: BoardType, player: Piece) -> int:
        return (
            self.WEIGHTS["victory"] * is_one_move_to_victory(board, player)
            + self.WEIGHTS["support"] * count_supporting_each_other(board, player)
            + self.WEIGHTS["covered_area"] * covered_area(board, player)
            + self.WEIGHTS["attacked"] * penalty_for_being_attacked(board, player)
            + self.WEIGHTS["advanced_enemy"]
            * most_advanced_piece(
                board, Piece.BLACK if player == Piece.WHITE else Piece.WHITE
            )
            + self.WEIGHTS["piece_difference"] * piece_difference(board, player)
        )
