from core.piece import Piece
from ai.heuristics.player_heuristics import most_advanced_piece

from test_utils import _, W, B


def test_most_advanced_piece_white_start_position():
    """White pieces are at the bottom row (y = 3). Expected advancement: 0."""
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [W, W, W, W]
    ]

    res = most_advanced_piece(board, Piece.WHITE)
    assert res == 0, f"Expected 0 advancement, got {res}"


def test_most_advanced_piece_black_start_position():
    """Black pieces are at the top row (y = 0). Expected advancement: 0."""
    board = [
        [B, B, B, B],
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]

    res = most_advanced_piece(board, Piece.BLACK)
    assert res == 0, f"Expected 0 advancement, got {res}"


def test_most_advanced_piece_white_advanced():
    """White piece is advanced to y = 1. Expected advancement: 4 - 1 - 1 = 2."""
    board = [
        [_, _, _, _],
        [_, W, _, _],
        [_, _, _, _],
        [W, _, W, W]
    ]

    res = most_advanced_piece(board, Piece.WHITE)
    assert res == 2, f"Expected 2 advancement, got {res}"


def test_most_advanced_piece_black_advanced():
    """Black piece is advanced to y = 3. Expected advancement: 3."""
    board = [
        [B, B, _, B],
        [_, _, _, _],
        [_, B, _, _],
        [_, _, B, _]
    ]

    res = most_advanced_piece(board, Piece.BLACK)
    assert res == 3, f"Expected 3 advancement, got {res}"
