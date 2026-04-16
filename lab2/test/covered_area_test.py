from core.piece import Piece
from ai.heuristics.player_heuristics import covered_area

from test_utils import (
    _, B, W
)

def test_white_cover_small_area():
    
    board = [
        [_, _, _, _],
        [_, W, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]

    res = covered_area(board, Piece.WHITE)
    assert 2 == res, f"Expected 2, got {res}"


def test_white_cover_big_area():
    
    board = [
        [_, _, W, _],
        [_, W, _, _],
        [W, _, W, _],
        [W, _, W, W]
    ]

    res = covered_area(board, Piece.WHITE)
    assert 7 == res, f"Expected 7, got {res}"

def test_black_cover_small_area():
    
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, B],
        [_, B, _, _]
    ]

    res = covered_area(board, Piece.BLACK)
    assert 1 == res, f"Expected 1, got {res}"


def test_black_cover_big_area():
    
    board = [
        [_, _, B, _],
        [_, B, _, _],
        [B, _, B, B],
        [B, _, B, B]
    ]

    res = covered_area(board, Piece.BLACK)
    assert 7 == res, f"Expected 7, got {res}"