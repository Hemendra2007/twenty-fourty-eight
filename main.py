import random
import copy
import json
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
FONT = pygame.font.SysFont('arial', 40)

def draw_board(screen, board, score, high_score):
    screen.fill(BACKGROUND_COLOR)
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = TILE_COLORS.get(value, TILE_COLORS[2048])
            pygame.draw.rect(screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE / 2, i * TILE_SIZE + TILE_SIZE / 2))
                screen.blit(text, text_rect)
    pygame.display.update()

def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    return board

def display_board(board):
    for row in board:
        print(row)
    print()

def add_random_tile(board):
    empty_positions = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
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
        new_row += [0] * (4 - len(new_row))
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
    if move == pygame.K_w or move == pygame.K_UP:
        return move_up(board)
    elif move == pygame.K_s or move == pygame.K_DOWN:
        return move_down(board)
    elif move == pygame.K_a or move == pygame.K_LEFT:
        return move_left(board)
    elif move == pygame.K_d or move == pygame.K_RIGHT:
        return move_right(board)
    return board, 0

def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

def save_game(board, score, high_score):
    game_state = {
        'board': board,
        'score': score,
        'high_score': high_score
    }
    with open('savegame.json', 'w') as f:
        json.dump(game_state, f)
    print("Game saved!")

def load_game():
    try:
        with open('savegame.json', 'r') as f:
            game_state = json.load(f)
        return game_state['board'], game_state['score'], game_state['high_score']
    except FileNotFoundError:
        print("No saved game found!")
        return initialize_board(), 0, 0

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
        print(f"New High Score: {high_score}")
    return high_score

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()
    load = input("Load saved game? (y/n): ")
    if load.lower() == 'y':
        game_board, score, high_score = load_game()
    else:
        game_board = initialize_board()
        add_random_tile(game_board)
        add_random_tile(game_board)
        score = 0
        high_score = 0

    display_board(game_board)
    print(f"Score: {score}")
    print(f"High Score: {high_score}")

    previous_board = copy.deepcopy(game_board)
    previous_score = score
    
     running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    previous_board = copy.deepcopy(game_board)
                    previous_score = score

                    new_board, move_score = handle_input(game_board, event.key)
                    if new_board != game_board:
                        game_board = new_board
                        score += move_score
                        add_random_tile(game_board)
                        draw_board(screen, game_board, score, high_score)
                        high_score = update_high_score(score, high_score)
                        if is_game_over(game_board):
                            print("Game Over! No more moves possible.")
                            print(f"Final Score: {score}")
                            running = False
                    else:
                        print("No valid move in that direction!")
                elif event.key == pygame.K_u:
                    game_board = previous_board
                    score = previous_score
                    draw_board(screen, game_board, score, high_score)
                elif event.key == pygame.K_s:
                    save_game(game_board, score, high_score)
                    print(f"Score: {score}")
                    print(f"High Score: {high_score}")

        draw_board(screen, game_board, score, high_score)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
