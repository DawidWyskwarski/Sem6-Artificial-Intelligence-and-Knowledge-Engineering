from core.piece import Piece
from ai.player_heuristics import piece_difference

from test_utils import _, B, W


def test_piece_difference_white_more_white_player():
    """White has 2 pieces, Black has 1. White player expectation: 1"""
    board = [
        [B, _, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [W, W, _, _]
    ]
    assert piece_difference(board, Piece.WHITE) == 1


def test_piece_difference_white_more_black_player():
    """White has 2 pieces, Black has 1. Black player expectation: -1"""
    board = [
        [B, _, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [W, W, _, _]
    ]
    assert piece_difference(board, Piece.BLACK) == -1


def test_piece_difference_black_more_black_player():
    """Black has 3 pieces, White has 1. Black player expectation: 2"""
    board = [
        [B, B, B, _],
        [_, _, _, _],
        [_, _, _, _],
        [W, _, _, _]
    ]
    assert piece_difference(board, Piece.BLACK) == 2


def test_piece_difference_equal_pieces():
    """Both have 2 pieces. Expected: 0 for both"""
    board = [
        [B, B, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [W, W, _, _]
    ]
    assert piece_difference(board, Piece.WHITE) == 0
    assert piece_difference(board, Piece.BLACK) == 0
