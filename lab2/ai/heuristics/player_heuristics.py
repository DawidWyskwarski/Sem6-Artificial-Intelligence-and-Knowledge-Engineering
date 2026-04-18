from core.piece import Piece
from core.game_utils import BoardType


def most_advanced_piece(board: BoardType, player: Piece) -> int:
    """
    Calculates the distance from the starting row of the player's most advanced piece.

    :param BoardType board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: The maximum distance advanced by any of the player's pieces.
    """

    max_advancement = 0
    height = len(board)

    for y, row in enumerate(board):
        for piece in row:
            if piece == player:
                advancement = (height - 1 - y) if player == Piece.WHITE else y

                if advancement > max_advancement:
                    max_advancement = advancement

    return max_advancement


def victory(board: BoardType, player: Piece) -> int:
    """
    Calculates a large heuristic reward if the given player has reached the target row.

    :param BoardType board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: 1000 if the player is in the victory position, otherwise 0.
    """

    one_from_victory_row = len(board) - 1 if player == Piece.BLACK else 0

    for piece in board[one_from_victory_row]:
        if piece == player:
            return 1000

    return 0


def piece_difference(board: BoardType, player: Piece) -> int:
    """
    Calculates the material difference in the number of pieces between the given player and the opponent.

    :param BoardType board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: The material difference (player's piece count minus opponent's piece count).
    """

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

def covered_area(board: BoardType, player: Piece) -> int:
    """
    Counts the individual squares covered by player pieces.

    :param BoardType board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: Covered individual squares.
    """

    delta = 1 if player == Piece.WHITE else -1

    height = len(board)
    width = len(board[0])

    covered_area = 0

    for y, row in enumerate(board):
        for x, _ in enumerate(row):
            delt_y = y + delta

            if 0 <= delt_y < height:
                if x - 1 >= 0 and board[delt_y][x-1] == player:
                    covered_area += 1
                elif x + 1 < width and board[delt_y][x+1] == player:
                    covered_area += 1

    return covered_area