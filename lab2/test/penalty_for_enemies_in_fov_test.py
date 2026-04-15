from core.piece import Piece
from ai.pieces_heuristics import penalty_for_enemies_in_fov

from test_utils import _, B, W


def test_fov_white_no_enemies():
    """White pieces have no black pieces in front of them."""
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [_, W, _, W]
    ]
    res = penalty_for_enemies_in_fov(board, Piece.WHITE)
    assert res == 0, f"Expected penalty 0, got {res}"


def test_fov_white_some_enemies():
    """White piece at (3, 1) sees black pieces at (2, 2), (1, 0), and (0, 1)."""
    board = [
        [_, B, _, _],
        [B, _, _, _],
        [_, _, B, _],
        [_, W, _, _]
    ]
    res = penalty_for_enemies_in_fov(board, Piece.WHITE)
    assert res == -3, f"Expected penalty -3, got {res}"


def test_fov_black_no_enemies():
    """Black pieces have no white pieces in front of them."""
    board = [
        [B, _, B, _],
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]
    res = penalty_for_enemies_in_fov(board, Piece.BLACK)
    assert res == 0, f"Expected penalty 0, got {res}"


def test_fov_black_some_enemies():
    """Black piece at (0, 2) sees white pieces at (1, 1), (2, 2), and (3, 3)."""
    board = [
        [_, _, B, _],
        [_, W, _, _],
        [_, _, W, _],
        [_, _, _, W]
    ]
    res = penalty_for_enemies_in_fov(board, Piece.BLACK)
    assert res == -3, f"Expected penalty -3, got {res}"


def test_fov_white_multiple_pieces_multiple_enemies():
    """Multiple White pieces evaluating multiple Black enemies in their respective FOVs."""
    board = [
        [_, B, _, B],
        [_, _, B, _],
        [_, _, _, _],
        [W, _, _, W]
    ]

    res = penalty_for_enemies_in_fov(board, Piece.WHITE)
    assert res == -3, f"Expected penalty -3, got {res}"


def test_fov_black_multiple_pieces_multiple_enemies():
    """Multiple Black pieces evaluating multiple White enemies in their respective FOVs."""
    board = [
        [B, _, B, _],
        [_, _, _, _],
        [_, W, _, _],
        [W, _, _, W]
    ]

    res = penalty_for_enemies_in_fov(board, Piece.BLACK)
    assert res == -4, f"Expected penalty -4, got {res}"
