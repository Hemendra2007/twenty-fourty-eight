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


class Game:
    def __init__(self):
        self.board = self.initialize_board()
        self.score = 0
        self.high_score = 0

    def initialize_board(self):
        board = [[0] * 4 for _ in range(4)]
        self.add_random_tile(board)
        self.add_random_tile(board)
        return board

    def add_random_tile(self, board):
        empty_positions = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_positions:
            i, j = random.choice(empty_positions)
            board[i][j] = random.choice([2, 4])

    def move_left(self):
        new_board = []
        score = 0
        for row in self.board:
            new_row = [num for num in row if num != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    score += new_row[i]
                    new_row[i + 1] = 0
            new_row = [num for num in new_row if num != 0]
            new_row += [0] * (4 - len(new_row))
            new_board.append(new_row)
        self.board = new_board
        return score

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        score = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return score

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        score = self.move_left()
        self.transpose()
        return score

    def move_down(self):
        self.transpose()
        score = self.move_right()
        self.transpose()
        return score

    def handle_input(self, move):
        if move == pygame.K_w or move == pygame.K_UP:
            score = self.move_up()
        elif move == pygame.K_s or move == pygame.K_DOWN:
            score = self.move_down()
        elif move == pygame.K_a or move == pygame.K_LEFT:
            score = self.move_left()
        elif move == pygame.K_d or move == pygame.K_RIGHT:
            score = self.move_right()
        else:
            return False

        if score > 0:
            self.score += score
            self.add_random_tile(self.board)
        return True

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
        return True

    def save_game(self):
        game_state = {
            'board': self.board,
            'score': self.score,
            'high_score': self.high_score
        }
        with open('savegame.json', 'w') as f:
            json.dump(game_state, f)
        print("Game saved!")

    def load_game(self):
        try:
            with open('savegame.json', 'r') as f:
                game_state = json.load(f)
            self.board = game_state['board']
            self.score = game_state['score']
            self.high_score = game_state['high_score']
            print("Game loaded!")
        except FileNotFoundError:
            print("No saved game found!")

    def reset_game(self):
        self.board = self.initialize_board()
        self.score = 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print(f"New High Score: {self.high_score}")


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


def draw_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    title_text = FONT.render("2048", True, (0, 0, 0))
    start_text = SMALL_FONT.render("Press 1 to Start Game", True, (0, 0, 0))
    instructions_text = SMALL_FONT.render("Press 2 for Instructions", True, (0, 0, 0))
    quit_text = SMALL_FONT.render("Press 3 to Quit", True, (0, 0, 0))

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.update()


def display_instructions(screen):
    screen.fill(BACKGROUND_COLOR)
    instructions = [
        "2048 Game Instructions:",
        "Use arrow keys (WASD or arrows) to move the tiles.",
        "Combine matching tiles to reach 2048.",
        "Press 'R' to reset the game.",
        "Press 'S' to save the game.",
        "Press 'U' to undo the last move.",
        "Press 'P' to pause.",
        "Press 'Q' to quit."
    ]
    y_offset = 50
    for line in instructions:
        instruction_text = SMALL_FONT.render(line, True, (0, 0, 0))
        screen.blit(instruction_text, (20, y_offset))
        y_offset += 30

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return


def game_mode_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    title_text = FONT.render("Select Mode", True, (0, 0, 0))
    classic_mode_text = SMALL_FONT.render("Press 1 for Classic Mode", True, (0, 0, 0))
    timed_mode_text = SMALL_FONT.render("Press 2 for Timed Mode", True, (0, 0, 0))

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(classic_mode_text, (WIDTH // 2 - classic_mode_text.get_width() // 2, HEIGHT // 2))
    screen.blit(timed_mode_text, (WIDTH // 2 - timed_mode_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'classic'
                elif event.key == pygame.K_2:
                    return 'timed'


def handle_menu_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start Game
                    return 'start'
                elif event.key == pygame.K_2:  # View Instructions
                    return 'instructions'
                elif event.key == pygame.K_3:  # Quit
                    pygame.quit()
                    quit()


def main_menu():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048 Menu')

    while True:
        draw_menu(screen)
        user_choice = handle_menu_input()
        if user_choice == 'start':
            game_mode = game_mode_menu(screen)  # Display the game mode menu
            break
        elif user_choice == 'instructions':
            display_instructions(screen)

    pygame.display.set_caption('2048')


def main():
    main_menu()  # Show the main menu before starting the game
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
                    display_instructions(screen)
                
                elif event.key == pygame.K_q:  # Quit game
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()
