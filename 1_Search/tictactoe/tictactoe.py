"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def empty_amount(board):
    amount = 0
    for row in board:
        for cell in row:
            if cell is EMPTY:
                amount = amount +1
    return amount


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if empty_amount(board)%2 == 1:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for row in range(3):
        for column in range(3):
            if board[row][column] is EMPTY:
                actions.append([row, column])
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    try:
        if result_board[action[0]][action[1]] is not EMPTY:
            raise IndexError
        else:
            result_board[action[0]][action[1]] = player(result_board)
            return result_board
    except IndexError:
        print('Spot already occupied')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # There can only be a winner if at least 5 pieces are on board
    if empty_amount(board) > 4:
        return None

    # I'm providing an easy to understand method, but there are more efficient ways to check

    # First we check in rows (in case the 3 are EMPTY, returns EMPTY, which is None)
    for row in range(0,3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return board[row][1]

    # Then we check in columns (in case the 3 are EMPTY, returns EMPTY, which is None)
    for column in range(0,3):
        if board[0][column] == board[1][column] and board[1][column] == board[2][column]:
            return board[1][column]
    
    # Finally we check both diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[1][1]
    
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or empty_amount(board) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) is None:
        return 0

    return 1 if winner(board) == X else -1

def minimax(board):
    current_player = player(board)

    if current_player == X:
        v = -math.inf
        for action in actions(board):
            k = min_value(result(board, action))    #FIXED
            if k > v:
                v = k
                best_move = action
    else:
        v = math.inf
        for action in actions(board):
            k = max_value(result(board, action))    #FIXED
            if k < v:
                v = k
                best_move = action
    return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v    #FIXED

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v    #FIXED
