from core.piece import Piece
from ai.pieces_heuristics import penalty_for_being_attacked

from test_utils import _, B, W


def test_penalty_attacking_white_none():
    """White pieces have no enemies attacking them."""
    board = [
        [_, _, _, _],
        [_, W, _, W],
        [_, _, _, _],
        [_, _, _, _]
    ]

    res = penalty_for_being_attacked(board, Piece.WHITE)
    assert res == 0, f"Expected 0, got {res}"


def test_penalty_attacking_white_lots():
    """Black pieces heavily attacked."""
    board = [
        [_, B, _, B, _],
        [_, _, W, _, _],
        [_, B, _, B, _],
        [W, _, W, _, W],
        [_, _, _, _, _],
    ]

    res = penalty_for_being_attacked(board, Piece.WHITE)
    assert res == -6, f"Expected -6, got {res}"


def test_penalty_attacking_black_none():
    """Black pieces aren't attacked."""
    board = [
        [_, _, _, _],
        [_, B, _, _],
        [_, _, _, _],
        [B, _, _, _]
    ]

    res = penalty_for_being_attacked(board, Piece.BLACK)
    assert res == 0, f"Expected 0 attacking, got {res}"


def test_penalty_attacking_black_lots():
    """Black pieces heavily attacked."""
    board = [
        [_, B, _, B, _],
        [B, _, W, _, B],
        [_, B, B, B, _],
        [W, W, W, W, W],
        [_, _, _, _, _],
    ]

    res = penalty_for_being_attacked(board, Piece.BLACK)
    assert res == -8, f"Expected -8, got {res}"
