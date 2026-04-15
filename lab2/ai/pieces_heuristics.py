from ai.ai_utils import count_pieces_diagonally
from core.game_state import BoardType
from core.piece import Piece


def count_supporting_each_other(board: BoardType, player: Piece) -> int:

    delta = 1 if player == Piece.BLACK else -1

    return count_pieces_diagonally(board, player, player, delta)


def penalty_for_being_attacked(board: BoardType, player: Piece) -> int:

    delta = 1 if player == Piece.BLACK else -1
    enemy = Piece.BLACK if player == Piece.WHITE else Piece.WHITE

    return -count_pieces_diagonally(board, player, enemy, delta)


def penalty_for_enemies_in_fov(board: BoardType, player: Piece) -> int:
    delta = 1 if player == Piece.BLACK else -1
    enemy = Piece.BLACK if player == Piece.WHITE else Piece.WHITE

    height = len(board)
    width = len(board[0]) if height > 0 else 0

    fov_score = 0

    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece == player:

                check_y = y + delta
                while 0 <= check_y < height:
                    for check_x in (x - 1, x, x + 1):
                        if 0 <= check_x < width:
                            if board[check_y][check_x] == enemy:
                                fov_score -= 1

                    check_y += delta

    return fov_score
