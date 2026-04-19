from ai.ai_utils import count_pieces_diagonally
from core.game_utils import Board
from core.piece import Piece
from core.game_utils import enemy_color


def count_supporting_each_other(board: Board, player: Piece) -> int:
    """
    Calculates a heuristic score based on how many of the player's pieces are supporting each other diagonally.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: The number of supporting piece pairs.
    """

    delta = 1 if player == Piece.BLACK else -1
    return count_pieces_diagonally(board, player, player, delta)


def penalty_for_being_attacked(board: Board, player: Piece) -> int:
    """
    Calculates a penalty heuristic based on the number of the player's pieces that are currently attacked by the enemy.

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: A negative integer representing the penalty for being attacked.
    """

    delta = 1 if player == Piece.BLACK else -1
    enemy = enemy_color(player)

    # This score is multiplied by -1 so if pieces are attacked by many enemies the game state score will decline.
    return -count_pieces_diagonally(board, player, enemy, delta)


def penalty_for_enemies_in_fov(board: Board, player: Piece) -> int:
    """
    Calculates a penalty heuristic based on the number of enemy pieces in the given player's field of view
    (the column to the left, the current column, and the column to the right).

    :param Board board: The current state of the board.
    :param Piece player: The player whose pieces are being evaluated.

    :return int: A negative integer representing the penalty for enemies in the field of view.
    """

    delta = 1 if player == Piece.BLACK else -1
    enemy = enemy_color(player)

    height = len(board)
    width = len(board[0])

    fov_score = 0

    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece != player:
                continue

            check_y = y + delta
            # Checking every square in (x-1,x,x+1) columns
            while 0 <= check_y < height:
                # Column on left
                if x - 1 >= 0 and board[check_y][x - 1] == enemy:
                    fov_score -= 1
                # Current column
                if board[check_y][x] == enemy:
                    fov_score -= 1
                # Current on right
                if x + 1 < width and board[check_y][x + 1] == enemy:
                    fov_score -= 1
                check_y += delta

    return fov_score
