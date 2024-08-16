import random
BOARD_SIZE = 4

def initialize_board():
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    return board

def display_board(board):
    for row in board:
        print(row)
    print()

def add_random_tile(board):
    empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
    if empty_positions:
        i, j = random.choice(empty_positions)
        board[i][j] = random.choice([2, 4])

def move_left(board):
    new_board = []
    score = 0
    for row in board:
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        new_row += [0] * (BOARD_SIZE - len(new_row))
        new_board.append(new_row)
    return new_board, score

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    new_board, score = move_left(reversed_board)
    return [row[::-1] for row in new_board], score
    
def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed_board = transpose(board)
    new_board, score = move_left(transposed_board)
    return transpose(new_board), score
    
def move_down(board):
    transposed_board = transpose(board)
    new_board, score = move_right(transposed_board)
    return transpose(new_board), score
    
def handle_input(board, move):
    if move == 'w':
        return move_up(board)
    elif move == 's':
        return move_down(board)
    elif move == 'a':
        return move_left(board)
    elif move == 'd':
        return move_right(board)
    return board
    
if __name__ == "__main__":
    game_board = initialize_board()
    add_random_tile(game_board)
    add_random_tile(game_board)
    display_board(game_board)
     while True:
        move = input("Enter move (w/a/s/d): ")
        if move in ['w', 'a', 's', 'd']:
            game_board = handle_input(game_board, move)
            add_random_tile(game_board)
            display_board(game_board)
        else:
            print("Invalid move! Please enter 'w', 'a', 's', or 'd'.")
