from core.game_utils import Board
from core.piece import Piece


def count_pieces_diagonally(
    board: Board, source_piece: Piece, target_piece: Piece, delta: int
) -> int:
    """
    Counts the number of `target_piece`s located diagonally adjacent to pieces of type `piece`.

    :param Board board: The current state of the board.
    :param Piece piece: The type of piece to check from.
    :param Piece target_piece: The type of piece to look for and count.
    :param int delta: The vertical offset representing the diagonal direction to check (e.g., 1 for forwards, -1 for backwards).

    :return int: The total count of `target_piece`s found in the specified diagonal positions.
    """

    count = 0
    height = len(board)
    width = len(board[0])

    for y in range(height):
        diag_y = y + delta
        # Check if the diagonal row is within the board bounds
        if 0 <= diag_y < height:
            row = board[y]
            for x, cell in enumerate(row):
                if cell == source_piece:
                    # Check diagonal left
                    if x - 1 >= 0 and board[diag_y][x - 1] == target_piece:
                        count += 1
                    # Check diagonal right
                    if x + 1 < width and board[diag_y][x + 1] == target_piece:
                        count += 1

    return count
