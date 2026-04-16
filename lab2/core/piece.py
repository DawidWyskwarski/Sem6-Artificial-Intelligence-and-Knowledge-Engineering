from enum import StrEnum


class Piece(StrEnum):
    """
    An enum representing the different types of pieces (and empty spaces) on the game board.
    Maps the string representation of each entity to a more readable constant.
    """
    WHITE = "W"
    BLACK = "B"
    EMPTY = "_"
