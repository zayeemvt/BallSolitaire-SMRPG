'''
   This generic solver attempts to find every possible solution given an
   initial configuration. This script shows that Ball Solitaire is only
   solvable when the empty space does NOT start on a corner or in the
   middle. All of the other remaining spaces produce initial states
   that are all rotations and/or reflections from one another. Thus, in
   its solvable form, Ball Solitaire has 210,422 possible move sequences
   that can solve the puzzle.
'''

from copy import deepcopy
from collections import deque

# Custom queue class used for breadth-first search
class StatesQueue:
    def __init__(self):
        self.queue = deque()

    def add_new_state(self, board, sequence):
        state = (board, sequence)
        self.queue.append(state)

    def pop(self):
        return self.queue.popleft()
    
    def isEmpty(self) -> bool:
        return len(self.queue) == 0

    def __str__(self):
        return str(self.queue)

'''
Generic solver functions
'''

# Function for finding all valid moves starting from a blank tile
def find_moves_from_blank(board, row, col):
    moves = []

    # Down
    if (row >= 2):
        if board[row-1][col] == 'O' and board[row-2][col] == 'O':
            moves.append((row-2, col, 'd'))

    # Up
    if (row <= 1):
        if board[row+1][col] == 'O' and board[row+2][col] == 'O':
            moves.append((row+2, col, 'u'))

    # Right
    if (col >= 2):
        if board[row][col-1] == 'O' and board[row][col-2] == 'O':
            moves.append((row, col-2, 'r'))

    # Left
    if (col <= 1):
        if board[row][col+1] == 'O' and board[row][col+2] == 'O':
            moves.append((row, col+2, 'l'))
    
    return moves

# Function for finding all valid moves starting from a ball tile
def find_moves_from_ball(board, row, col):
    moves = []

    # Up
    if (row >= 2):
        if board[row-1][col] == 'O' and board[row-2][col] == ' ':
            moves.append((row, col, 'u'))

    # Down
    if (row <= 1):
        if board[row+1][col] == 'O' and board[row+2][col] == ' ':
            moves.append((row, col, 'd'))

    # Left
    if (col >= 2):
        if board[row][col-1] == 'O' and board[row][col-2] == ' ':
            moves.append((row, col, 'l'))

    # Right
    if (col <= 1):
        if board[row][col+1] == 'O' and board[row][col+2] == ' ':
            moves.append((row, col, 'r'))
    
    return moves

# Generates a list of all possible moves within the board
def find_valid_moves(board, count):
    valid_moves = []

    for i in range(0,4):
        for j in range(0,4):

            '''
            For optimization, check moves on blank tiles when there are
            fewer blank tiles than balls. This is usually the case
            during the first half of the move sequence.

            Similarly, check moves on ball tiles when there are fewer
            ball tiles than blanks. This is usually the case during the
            back half of the move sequence.
            '''
            
            # Check blank tiles...
            if board[i][j] != 'O' and count < 7:
                possible_moves = find_moves_from_blank(board, i, j)

                if (len(possible_moves) > 0):
                    valid_moves += possible_moves
            
            # ... or check ball tiles
            elif board[i][j] == 'O' and count >= 7:
                possible_moves = find_moves_from_ball(board, i, j)

                if (len(possible_moves) > 0):
                    valid_moves += possible_moves
    
    return valid_moves

# Creates a copy of the board with the specified move taken
def process_move(board, move):
    new_board = deepcopy(board)

    down_dir = 0
    right_dir = 0

    match move[2]:
        case 'd':
            down_dir = 1

        case 'u':
            down_dir = -1

        case 'r':
            right_dir = 1

        case 'l':
            right_dir = -1

    new_board[move[0]][move[1]] = ' '
    new_board[move[0] + down_dir][move[1] + right_dir] = ' '
    new_board[move[0] + 2*down_dir][move[1] + 2*right_dir] = 'O'

    return new_board
    



## Main code

def main():
    states_queue = StatesQueue()
    solved_states = StatesQueue()

    start = (0,2)

    start_board = [['O' for _ in range(4)] for _ in range(4)]
    start_board[start[0]][start[1]] = ' '
    start_move_sequence = []

    states_queue.add_new_state(start_board, start_move_sequence)

    iteration = 0

    while(not states_queue.isEmpty()):
        current_state = states_queue.pop()

        moves_to_check = find_valid_moves(current_state[0], len(current_state[1]))

        for move in moves_to_check:
            new_board = process_move(current_state[0], move)
            new_sequence = list(current_state[1])
            new_sequence.append(move)

            if len(new_sequence) == 14:
                solved_states.add_new_state(new_board, new_sequence)
            else:
                states_queue.add_new_state(new_board, new_sequence)
        
        iteration += 1

        if (iteration % 15000 == 0):
            print(f'{len(states_queue.queue)} states found, {len(solved_states.queue)} solutions found, last sequence length: {len(new_sequence)}')

    print(f'There are {len(solved_states.queue)} solutions.')

main()