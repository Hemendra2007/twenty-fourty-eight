import pygame
import random
import copy
import json

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
SMALL_FONT = pygame.font.SysFont('arial', 20)

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
    score_text = SMALL_FONT.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = SMALL_FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 30))

    restart_button = pygame.Rect(250, 10, 100, 40)
    pygame.draw.rect(screen, (0, 255, 0), restart_button)
    restart_text = SMALL_FONT.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, (270, 20))

    quit_button = pygame.Rect(250, 60, 100, 40)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = SMALL_FONT.render("Quit", True, (0, 0, 0))
    screen.blit(quit_text, (280, 70))

    pygame.display.update()

def draw_game_over(screen, score):
    screen.fill(BACKGROUND_COLOR)
    game_over_text = FONT.render("Game Over!", True, (255, 0, 0))
    score_text = SMALL_FONT.render(f"Final Score: {score}", True, (0, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
    pygame.display.update()
    pygame.time.wait(3000)

def draw_victory(screen, score):
    screen.fill(BACKGROUND_COLOR)
    victory_text = FONT.render("You Win!", True, (0, 255, 0))
    score_text = SMALL_FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + victory_text.get_height()))
    pygame.display.update()
    pygame.time.wait(3000)

def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    return board

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

def animate_move(screen, old_board, new_board, score, high_score, move):
    steps = 10
    delay = 50  

    for step in range(steps):
        interpolated_board = copy.deepcopy(old_board)
        for i in range(4):
            for j in range(4):
                if old_board[i][j] != new_board[i][j]:
                    if move == 'left':
                        new_x = j * TILE_SIZE - step * TILE_SIZE / steps
                        new_rect = pygame.Rect(new_x, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    elif move == 'right':
                        new_x = j * TILE_SIZE + step * TILE_SIZE / steps
                        new_rect = pygame.Rect(new_x, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    elif move == 'up':
                        new_y = i * TILE_SIZE - step * TILE_SIZE / steps
                        new_rect = pygame.Rect(j * TILE_SIZE, new_y, TILE_SIZE, TILE_SIZE)
                    elif move == 'down':
                        new_y = i * TILE_SIZE + step * TILE_SIZE / steps
                        new_rect = pygame.Rect(j * TILE_SIZE, new_y, TILE_SIZE, TILE_SIZE)

                    color = TILE_COLORS.get(old_board[i][j], TILE_COLORS[2048])
                    pygame.draw.rect(screen, color, new_rect)
                    if old_board[i][j] != 0:
                        text = FONT.render(str(old_board[i][j]), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(new_rect.x + TILE_SIZE / 2, new_rect.y + TILE_SIZE / 2))
                        screen.blit(text, text_rect)

        draw_board(screen, interpolated_board, score, high_score)
        pygame.time.delay(delay)
        pygame.display.flip()

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

    draw_board(screen, game_board, score, high_score)

    previous_boards = [copy.deepcopy(game_board)]
    previous_scores = [score]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    previous_boards.append(copy.deepcopy(game_board))
                    previous_scores.append(score)

                    new_board, move_score = handle_input(game_board, event.key)
                    if new_board != game_board:
                        direction = None
                        if event.key in [pygame.K_w, pygame.K_UP]:
                            direction = 'up'
                        elif event.key in [pygame.K_s, pygame.K_DOWN]:
                            direction = 'down'
                        elif event.key in [pygame.K_a, pygame.K_LEFT]:
                            direction = 'left'
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            direction = 'right'

                        animate_move(screen, game_board, new_board, score, high_score, direction)
                        
                        game_board = new_board
                        score += move_score
                        add_random_tile(game_board)
                        draw_board(screen, game_board, score, high_score)
                        high_score = update_high_score(score, high_score)

                        if any(2048 in row for row in game_board):
                            draw_victory(screen, score)
                            running = False

                        if is_game_over(game_board):
                            draw_game_over(screen, score)
                            running = False
                    else:
                        print("No valid move in that direction!")
                elif event.key == pygame.K_u:
                    if len(previous_boards) > 1:
                        previous_boards.pop()
                        game_board = previous_boards[-1]
                        score = previous_scores.pop()
                        draw_board(screen, game_board, score, high_score)
                elif event.key == pygame.K_s:
                    save_game(game_board, score, high_score)
                    print(f"Score: {score}")
                    print(f"High Score: {high_score}")

        draw_board(screen, game_board, score, high_score)
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
