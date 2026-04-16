from core.piece import Piece
from ai.heuristics.pieces_heuristics import count_supporting_each_other

from test_utils import (
    _, B, W
)

def test_count_supporting_white_none():
    """White pieces have no support (no friendly pieces diagonally behind them)."""
    board = [
        [_, _, _, _],
        [_, W, _, W],
        [_, _, _, _],
        [_, _, _, _]
    ]
    
    res = count_supporting_each_other(board, Piece.WHITE)
    assert res == 0, f"Expected 0 supports, got {res}"

def test_count_supporting_white_lots():
    """White pieces are in a pyramid, heavily supporting each other."""
    board = [
        [_, _, _, _, _],
        [_, _, W, _, _],
        [_, W, _, W, _],
        [W, _, W, _, W],
        [_, _, _, _, _]
    ]
    
    res = count_supporting_each_other(board, Piece.WHITE)
    assert res == 6, f"Expected 6 supports, got {res}"

def test_count_supporting_black_none():
    """Black pieces have no support (no friendly pieces diagonally behind them)."""
    board = [
        [_, _, _, _],
        [_, B, _, _],
        [_, _, _, _],
        [B, _, _, _]
    ]
    
    res = count_supporting_each_other(board, Piece.BLACK)
    assert res == 0, f"Expected 0 supports, got {res}"

def test_count_supporting_black_lots():
    """Black pieces in an inverted pyramid form, heavily supporting each other."""
    board = [
        [_, _, _, _, _],
        [B, _, B, _, B],
        [_, B, _, B, _],
        [_, _, B, _, _],
        [_, _, _, _, _]
    ]
    
    res = count_supporting_each_other(board, Piece.BLACK)
    assert res == 6, f"Expected 6 supports, got {res}"

