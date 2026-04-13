from typing import List

ROWS_PER_SIDE: int = 2
'''
Constant value representing how many rows of each pieces there are.
'''

def initialize_default_board(width: int = 8, height: int =8) -> List[List[str]]:
    '''
    Method generating default setting of a board for given dimensions. 
    '''

    #[['B'] * width] * ROWS_PER_SIDE - rows of black (B) pieces
    #[['_'] * width] * (height-4) - rows with no pieces
    #[['W'] * width] * ROWS_PER_SIDE - rows of white (W) pieces 
    return [['B']*width]*ROWS_PER_SIDE + [['_']*width]*(height-4) + [['W']*width]*ROWS_PER_SIDE 

