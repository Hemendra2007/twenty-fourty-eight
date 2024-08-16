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

def move_left(board):
    new_board = []
    for row in board:
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        new_row += [0] * (BOARD_SIZE - len(new_row))
        new_board.append(new_row)
    return new_board

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    new_board = move_left(reversed_board)
    return [row[::-1] for row in new_board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed_board = transpose(board)
    new_board = move_left(transposed_board)
    return transpose(new_board)

def move_down(board):
    transposed_board = transpose(board)
    new_board = move_right(transposed_board)
    return transpose(new_board)


if __name__ == "__main__":
    game_board = initialize_board()
    add_random_tile(game_board)
    add_random_tile(game_board)
    display_board(game_board)
    print("\nAfter moving left:\n")
    game_board = move_left(game_board)
    display_board(game_board)
