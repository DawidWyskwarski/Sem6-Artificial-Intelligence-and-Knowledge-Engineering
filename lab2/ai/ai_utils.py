from core.game_state import BoardType
from core.piece import Piece


def count_pieces_diagonally(
    board: BoardType, piece: Piece, target_piece: Piece, delta: int
) -> int:
    count = 0
    height = len(board)
    width = len(board[0])

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == piece:
                diag_y = y + delta

                # Check if the diagonal row is within the board bounds
                if 0 <= diag_y < height:

                    # Check bottom-left (or top-left for black)
                    if x - 1 >= 0 and board[diag_y][x - 1] == target_piece:
                        count += 1

                    # Check bottom-right (or top-right for black)
                    if x + 1 < width and board[diag_y][x + 1] == target_piece:
                        count += 1

    return count
