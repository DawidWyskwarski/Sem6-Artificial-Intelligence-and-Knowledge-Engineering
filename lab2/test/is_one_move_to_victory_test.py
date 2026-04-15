from core.piece import Piece
from ai.player_heuristics import is_one_move_to_victory

from test_utils import _, B, W


def test_is_one_move_to_victory_white_true():
    """White is one move away (y=1). Expected 1000."""
    board = [
        [_, _, _, _],
        [_, W, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]
    assert is_one_move_to_victory(board, Piece.WHITE) == 1000


def test_is_one_move_to_victory_white_false():
    """White is not one move away (y=2, y=3). Expected 0."""
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, W, _, _],
        [W, _, _, _]
    ]
    assert is_one_move_to_victory(board, Piece.WHITE) == 0


def test_is_one_move_to_victory_black_true():
    """Black is one move away (y=2 on a 4-row board). Expected 1000."""
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, B, _, _],
        [_, _, _, _]
    ]
    assert is_one_move_to_victory(board, Piece.BLACK) == 1000


def test_is_one_move_to_victory_black_false():
    """Black is not one move away (y=0, y=1). Expected 0."""
    board = [
        [B, _, _, _],
        [_, B, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]
    assert is_one_move_to_victory(board, Piece.BLACK) == 0
