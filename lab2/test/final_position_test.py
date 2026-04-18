from core.piece import Piece
from ai.heuristics.player_heuristics import victory
from core.game_state import GameState

from test_utils import _, B, W

def is_final_white():
    board = [
        [_, W, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _]
    ]

    game_state = GameState(board)

    res = game_state.is_final()

    assert res == (True, W), f"Expected white's final possition, got {res} instead"


def is_final_black():
    board = [
        [_, _, _, _],
        [_, _, _, _],
        [_, _, _, _],
        [_, B, _, _]
    ]

    game_state = GameState(board)

    res = game_state.is_final()

    assert res == (True, B), f"Expected black's final possition, got {res} instead"

def is_not_final():
    board = [
        [_, _, _, _],
        [_, W, _, _],
        [_, B, _, _],
        [_, _, _, _]
    ]

    game_state = GameState(board)

    res = game_state.is_final()

    assert res == (False, None), f"Expected no final possition, got {res} instead"