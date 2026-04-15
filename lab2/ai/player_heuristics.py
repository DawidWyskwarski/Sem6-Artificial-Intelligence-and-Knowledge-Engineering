from typing import List

from core.piece import Piece
from core.game_state import BoardType


def most_advanced_piece(board: BoardType, player: Piece) -> int:
    max_advancement = 0
    height = len(board)

    for y, row in enumerate(board):
        for piece in row:
            if piece == player:
                advancement = (height - 1 - y) if player == Piece.WHITE else y

                if advancement > max_advancement:
                    max_advancement = advancement

    return max_advancement


def is_one_move_to_victory(board: BoardType, player: Piece) -> int:

    one_from_victory_row = len(board) - 2 if player == Piece.BLACK else 1

    for piece in board[one_from_victory_row]:
        if piece == player:
            return 1000

    return 0


def piece_difference(board: BoardType, player: Piece) -> int:

    white_count = 0
    black_count = 0

    for row in board:
        for piece in row:
            if piece == Piece.WHITE:
                white_count += 1
            elif piece == Piece.BLACK:
                black_count += 1

    return (
        black_count - white_count
        if player == Piece.BLACK
        else white_count - black_count
    )
