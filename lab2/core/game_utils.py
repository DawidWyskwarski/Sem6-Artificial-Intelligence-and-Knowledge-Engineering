from typing import List
from core.piece import Piece

type BoardType = List[List[Piece]]

ROWS_PER_SIDE: int = 2
"""
Constant value representing how many rows of pieces there are on each side.
"""


def initialize_default_board(width: int = 8, height: int = 8) -> BoardType:
    """
    Method generating default setting of a board for given dimensions.
    """

    # [[Piece.BLACK] * width] * ROWS_PER_SIDE - rows of black (B) pieces
    # [[Piece.EMPTY] * width] * (height-4) - rows with no pieces
    # [[PIECE.WHITE] * width] * ROWS_PER_SIDE - rows of white (W) pieces
    return (
        [[Piece.BLACK] * width for _ in range(ROWS_PER_SIDE)]
        + [[Piece.EMPTY] * width for _ in range(height - 4)]
        + [[Piece.WHITE] * width for _ in range(ROWS_PER_SIDE)]
    )


def is_legal_diagonal(square: Piece, enemy: Piece) -> bool:
    """
    A piece can move one square diagonally forward into an empty square or to capture an enemy piece.
    """
    return square in [Piece.EMPTY, enemy]


def is_legal_straight(square: Piece) -> bool:
    """
    A piece can move one square straight forward into an empty square.
    """
    return square == Piece.EMPTY
