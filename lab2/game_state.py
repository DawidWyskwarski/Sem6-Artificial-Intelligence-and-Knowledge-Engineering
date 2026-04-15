from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass

from piece import Piece
from utils import (
    initialize_default_board, is_legal_diagonal, 
    is_legal_straight
)

class GameState():

    @dataclass
    class Coordinate:
        '''
        Representation of the coordinates on the board.
        Used as a structured object to enhance readability over generic tuples.

        Doesn't guarantee being in the scope of the board.
        '''
        x: int
        y: int

    _board: List[List[Piece]]

    def __init__(self, board: List[List[Piece]] | None = None) -> None:
        '''
        Base constructor.
        '''
        self._board = board if board is not None else initialize_default_board()

    @classmethod
    def default_from_dimensions(cls, width: int, height: int) -> GameState:
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

    def _move_piece(self, start: Coordinate, end: Coordinate) -> GameState:
        '''
        Move a piece from one square to another on a board. 
        Only to be used after the legality check of the move.

        :param Coordinate start: square from where the piece is moved
        :param Coordinate end: square to where the piece is moved
        :return: GameState object representing a new state.
        '''

        # Perform a deep copy of the 2D list to avoid mutating the original board
        new_state = [row[:] for row in self._board]
        
        # Access the board as: board[row_index][column_index], which translates to board[y][x]
        tmp = new_state[start.y][start.x]

        new_state[start.y][start.x] = Piece.EMPTY
        new_state[end.y][end.x] = tmp

        return GameState(new_state)

    def _get_legal_moves(self, turn: Piece) -> List[Tuple[Coordinate, Coordinate]]:
        '''
        Finds all legal moves for a given player according to Breakthrough rules.
        
        Game Rules matches:
        - A piece can move one square straight forward if it is empty.
        - A piece can move one square diagonally forward to an empty square, or to capture an enemy piece.
        
        :param Piece turn: The player whose turn it is (Piece.WHITE or Piece.BLACK).
        :return: A list of legal moves as tuples of (start_coordinate, end_coordinate).
        '''
        if turn == Piece.EMPTY:
            raise RuntimeError('Turn must be either Whites or Blacks')
        
        # Parametrization variable so we have 1 method covering both turns
        delta = -1 if turn == Piece.WHITE else 1
        
        enemy = Piece.BLACK if turn == Piece.WHITE else Piece.WHITE
        
        moves = []

        for y, row in enumerate(self._board):
            for x, piece in enumerate(row):
                # Skip squares that do not belong to the current player
                if piece != turn:
                    continue
                
                coords = self.Coordinate(x, y)
                next_y = y + delta
                
                # Check for bounds if y + delta reaches the end of the board
                # It shouldn't happen but just in case.
                if 0 <= next_y < len(self._board):

                    if x - 1 >= 0 and is_legal_diagonal(self._board[next_y][x - 1], enemy):
                        moves.append( (coords, self.Coordinate(x - 1, next_y)) )
                    
                    if is_legal_straight(self._board[next_y][x]):
                        moves.append( (coords, self.Coordinate(x, next_y)) )
                    
                    if x + 1 < len(row) and is_legal_diagonal(self._board[next_y][x + 1], enemy):
                        moves.append( (coords, self.Coordinate(x + 1, next_y)) )
        
        return moves

    def generate_states(self, turn: Piece) -> List[GameState]:
        '''
        Generate a list of possible game states from current state.

        :param Piece turn: whose turn is now.
        :return: list of `GameState` objects
        :raises RuntimeError: When turn is passed as `Piece.EMPTY`
        '''
        
        if turn == Piece.EMPTY:
            raise RuntimeError('Turn must be either Whites or Blacks')

        # 1. Get the abstract moves (start -> end)
        valid_moves = self._get_legal_moves(turn)
        
        # 2. Map the moves to actual GameState objects
        new_states = [self._move_piece(start, end) for start, end in valid_moves]

        return new_states
    
