import random
BOARD_SIZE = 4

def initialize_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    return board

def display_board(board):
    for row in board:
        print(row)

def add_random_tile(board):
    empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
    if empty_positions:
        i, j = random.choice(empty_positions)
        board[i][j] = random.choice([2, 4])

if __name__ == "__main__":
    game_board = initialize_board()
    add_random_tile(game_board)
    add_random_tile(game_board)
    display_board(game_board)
