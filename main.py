import random
import copy
import json
import pygame

pygame.init()
WIDTH, HEIGHT = 400, 500
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
SMALL_FONT = pygame.font.SysFont('arial', 24)

def draw_board(screen, board, score, high_score):
    if score < 1000:
        screen.fill(BACKGROUND_COLOR)
    elif score < 5000:
        screen.fill((210, 180, 140))  # Light Brown
    elif score < 10000:
        screen.fill((144, 238, 144))  # Light Green
    else:
        screen.fill((135, 206, 250))  # Sky Blue
    
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
    screen.blit(score_text, (10, HEIGHT - 90))
    screen.blit(high_score_text, (10, HEIGHT - 60))
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

def animate_move(screen, old_board, new_board, score, high_score, direction):
    steps = 10
    delay = 20  # milliseconds

    old_positions = {(i, j): (i, j) for i in range(4) for j in range(4) if old_board[i][j] != 0}
    for step in range(steps + 1):
        screen.fill(BACKGROUND_COLOR)
        for i in range(4):
            for j in range(4):
                value = old_board[i][j]
                if value != 0:
                    start_pos = old_positions.get((i, j), (i, j))
                    end_pos = (i, j)
                    if direction == 'left':
                        new_pos = (start_pos[0], start_pos[1] - (start_pos[1] - end_pos[1]) * step / steps)
                    elif direction == 'right':
                        new_pos = (start_pos[0], start_pos[1] + (end_pos[1] - start_pos[1]) * step / steps)
                    elif direction == 'up':
                        new_pos = (start_pos[0] - (start_pos[0] - end_pos[0]) * step / steps, start_pos[1])
                    elif direction == 'down':
                        new_pos = (start_pos[0] + (end_pos[0] - start_pos[0]) * step / steps, start_pos[1])

                    new_pos = (int(new_pos[1] * TILE_SIZE), int(new_pos[0] * TILE_SIZE))
                    color = TILE_COLORS.get(value, TILE_COLORS[2048])
                    pygame.draw.rect(screen, color, (new_pos[1], new_pos[0], TILE_SIZE, TILE_SIZE))
                    text = FONT.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(new_pos[1] + TILE_SIZE / 2, new_pos[0] + TILE_SIZE / 2))
                    screen.blit(text, text_rect)

        score_text = SMALL_FONT.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = SMALL_FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, HEIGHT - 90))
        screen.blit(high_score_text, (10, HEIGHT - 60))
        pygame.display.update()
        pygame.time.delay(delay)

def pause_game(screen):
    paused = True
    pause_text = FONT.render("Game Paused", True, (0, 0, 0))
    screen.blit(pause_text, (WIDTH // 4, HEIGHT // 2 - 20))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume with 'R'
                    paused = False

def display_instructions(screen):
    instructions = [
        "Use W/A/S/D or Arrow keys to move tiles.",
        "Press R to Reset game.",
        "Press U to Undo move.",
        "Press S to Save game.",
        "Press P to Pause game.",
        "Press Q to Quit game."
    ]
    font = pygame.font.SysFont('arial', 24)
    screen.fill(BACKGROUND_COLOR)
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, (0, 0, 0))
        screen.blit(text, (10, 10 + i * 30))
    pygame.display.update()
    pygame.time.wait(5000)

class Game:
    def __init__(self):
        self.board = initialize_board()
        add_random_tile(self.board)
        add_random_tile(self.board)
        self.score = 0
        self.high_score = 0

    def reset_game(self):
        self.board = initialize_board()
        add_random_tile(self.board)
        add_random_tile(self.board)
        self.score = 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print(f"New High Score: {self.high_score}")

    def save_game(self):
        save_game(self.board, self.score, self.high_score)

    def load_game(self):
        self.board, self.score, self.high_score = load_game()
    
    def handle_input(self, move):
        new_board, move_score = handle_input(self.board, move)
        if new_board != self.board:
            direction = None
            if move in [pygame.K_w, pygame.K_UP]:
                direction = 'up'
            elif move in [pygame.K_s, pygame.K_DOWN]:
                direction = 'down'
            elif move in [pygame.K_a, pygame.K_LEFT]:
                direction = 'left'
            elif move in [pygame.K_d, pygame.K_RIGHT]:
                direction = 'right'

            animate_move(screen, self.board, new_board, self.score, self.high_score, direction)

            self.board = new_board
            self.score += move_score
            add_random_tile(self.board)
            self.update_high_score()
            return not is_game_over(self.board)
        return True

def main():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()
    
    display_instructions(screen)
    
    game = Game()
    
    load = input("Load saved game? (y/n): ")
    if load.lower() == 'y':
        game.load_game()

    draw_board(screen, game.board, game.score, game.high_score)
    
    previous_board = copy.deepcopy(game.board)
    previous_score = game.score
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    previous_board = copy.deepcopy(game.board)
                    previous_score = game.score

                    if not game.handle_input(event.key):
                        print("Game Over!")
                        running = False
                        break

                    draw_board(screen, game.board, game.score, game.high_score)

                elif event.key == pygame.K_r:  # Reset game
                    game.reset_game()
                    draw_board(screen, game.board, game.score, game.high_score)
                
                elif event.key == pygame.K_u:  # Undo move
                    game.board = previous_board
                    game.score = previous_score
                    draw_board(screen, game.board, game.score, game.high_score)
                
                elif event.key == pygame.K_s:  # Save game
                    game.save_game()
                
                elif event.key == pygame.K_p:  # Pause game with 'P'
                    pause_game(screen)
                
                elif event.key == pygame.K_q:  # Quit game
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
