"""
Tic Tac Toe Player
"""

import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if empty_amount(board)%2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in board:
        for cell in row:
            if cell is EMPTY:
                actions.add((cell, row))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board(action[0], action[1]) = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # There can only be a winner if at least 5 pieces are on board
    if empty_amount > 4:
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
    if winner(board) != None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner = winner(board)
    if winner is None:
        return 0
    return 1 if winner == X else -1

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
