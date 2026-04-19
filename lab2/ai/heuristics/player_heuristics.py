from core.piece import Piece
from core.game_utils import Board


def most_advanced_piece(board: Board, player: Piece) -> int:
    """
    Calculates the distance from the starting row of the player's most advanced piece.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: The maximum distance advanced by any of the player's pieces.
    """

    height = len(board)

    # Based on the player we either go from the start or from the end. 
    if player == Piece.WHITE:
        y_range = range(height)
    else:
        y_range = range(height - 1, -1, -1)

    for y in y_range:
        row = board[y]
        for piece in row:
            if piece == player:
                return (height - 1 - y) if player == Piece.WHITE else y

    return -1


def victory_reward(board: Board, player: Piece) -> int:
    """
    Calculates a large heuristic reward if the given player has reached the target row.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: 1000 if the player is in the victory position, otherwise 0.
    """

    victory_row = len(board) - 1 if player == Piece.BLACK else 0

    for piece in board[victory_row]:
        if piece == player:
            return 1000

    return 0


def piece_difference(board: Board, player: Piece) -> int:
    """
    Calculates the material difference in the number of pieces between the given player and the opponent.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: The material difference (player's piece count minus opponent's piece count).
    """

    white_count = 0

    for row in board:
        for piece in row:
            if piece == Piece.WHITE:
                white_count += 1
            elif piece == Piece.BLACK:
                white_count -= 1

    return (
        -white_count
        if player == Piece.BLACK
        else white_count
    )

def covered_area(board: Board, player: Piece) -> int:
    """
    Counts the individual squares covered by player pieces.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: Covered individual squares.
    """

    delta = 1 if player == Piece.WHITE else -1

    height = len(board)
    width = len(board[0])

    area_score = 0

    for y in range(height):
        delt_y = y + delta
        if 0 <= delt_y < height:
            for x in range(width):
                if x - 1 >= 0 and board[delt_y][x-1] == player:
                    area_score += 1
                elif x + 1 < width and board[delt_y][x+1] == player:
                    area_score += 1

    return area_score