from typing import List

from board_utils import initialize_default_board

class _BoardMeta(type):
    '''
    Necessary for the Board class to be a Singleton.
    '''
    _instances = {}
    
    def __call__(cls, *args, **kwds):
        
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Board(metaclass=_BoardMeta):
    '''
    Singleton class representing current board state.
    '''

    _board: List[List[str]]

    def __init__(self, board: List[List[str]] = None) -> None:
        '''
        Base constructor.
        '''
        self._board = board if board is not None else initialize_default_board()

    @classmethod
    def from_dimensions(cls, width: int, height: int) -> Board:
        '''
        Alternative constructor for width and height.
        '''
        return cls(initialize_default_board(width, height))
    
    def __str__(self) -> str:
        '''
        Current state of a board formatted for print
        '''
        width = len(self._board[0]) * 2 + 1
        border = f"+{'-' * width}+"
        
        return f"{border}\n" + "\n".join(f"| {' '.join(row)} |" for row in self._board) + f"\n{border}"

    