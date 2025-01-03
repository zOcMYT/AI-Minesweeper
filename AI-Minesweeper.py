import pygame
import random

# Constants
CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 10
NUM_MINES = 10

# RGB Colors
BACKGROUND_COLOR = (18, 18, 18)  # Dark background
CELL_COLOR = (34, 34, 34)  # Slightly lighter dark for covered cells
MINE_COLOR = (255, 0, 0)  # Bright red for mines
FLAG_COLOR = (255, 215, 0)  # Gold for flags

# Vibrant number colors
NUMBER_COLORS = {
    1: (0, 255, 0),    # Bright green
    2: (0, 191, 255),  # Deep sky blue
    3: (255, 165, 0),  # Orange
    4: (75, 0, 130),   # Indigo
    5: (255, 20, 147), # Deep pink
    6: (0, 255, 255),  # Cyan
    7: (255, 255, 0),  # Yellow
    8: (128, 0, 128),  # Purple
}

class Minesweeper:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.num_mines = NUM_MINES
        self.board = self.create_board()
        self.visible = [[False] * self.width for _ in range(self.height)]
        self.game_over = False
        self.flags = [[False] * self.width for _ in range(self.height)]  # Track flags

    def create_board(self):
        board = [[0] * self.width for _ in range(self.height)]
        mine_positions = set()

        while len(mine_positions) < self.num_mines:
            pos = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if pos not in mine_positions:
                mine_positions.add(pos)
                board[pos[0]][pos[1]] = -1  # Place a mine
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= pos[0] + dy < self.height and 0 <= pos[1] + dx < self.width and (dx != 0 or dy != 0):
                            if board[pos[0] + dy][pos[1] + dx] != -1:
                                board[pos[0] + dy][pos[1] + dx] += 1
        return board

    def reveal(self, x, y):
        if self.game_over or self.visible[y][x]:
            return

        if self.board[y][x] == -1:  # Mine clicked
            self.game_over = True  # Set game over
            self.reveal_all_mines()  # Reveal all mines
            return

        self.visible[y][x] = True
        if self.board[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= y + dy < self.height and 0 <= x + dx < self.width:
                        self.reveal(x + dx, y + dy)

    def reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    self.visible[y][x] = True

    def flag(self, x, y):
        if not self.visible[y][x]:
            self.flags[y][x] = not self.flags[y][x]  # Toggle flag state

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.visible[y][x]:
                    return False
        return True

    def draw_flag(self, screen, x, y):
        # Draw a flag marker
        pygame.draw.rect(screen, FLAG_COLOR, (x * CELL_SIZE + 15, y * CELL_SIZE + 10, 5, 20))  # Flag pole
        pygame.draw.polygon(screen, FLAG_COLOR, [
            (x * CELL_SIZE + 15, y * CELL_SIZE + 10),
            (x * CELL_SIZE + 30, y * CELL_SIZE + 20),
            (x * CELL_SIZE + 15, y * CELL_SIZE + 20)
        ])  # Flag triangle

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)  # Dark background

        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.visible[y][x]:
                    if self.board[y][x] == -1:
                        pygame.draw.rect(screen, MINE_COLOR, rect)  # Show mine
                    else:
                        # Draw a vibrant gradient for visible cells
                        color = (100 + self.board[y][x] * 20, 100 + self.board[y][x] * 10, 100)
                        pygame.draw.rect(screen, color, rect)
                        if self.board[y][x] > 0:
                            font = pygame.font.SysFont(None, 36)
                            text_color = NUMBER_COLORS.get(self.board[y][x], (255, 255, 255))  # Default to white
                            text = font.render(str(self.board[y][x]), True, text_color)
                            screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))
                else:
                    pygame.draw.rect(screen, CELL_COLOR, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border for covered cell

                    # Draw flags if placed
                    if self.flags[y][x]:
                        self.draw_flag(screen, x, y)

        # Draw win or game over messages
        if self.game_over:
            self.display_message(screen, "Game Over!", (255, 0, 0))
        if self.check_win():
            self.display_message(screen, "You Win!", (0, 255, 0))

    def display_message(self, screen, message, color):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width * CELL_SIZE, self.height * CELL_SIZE))
        overlay.set_alpha(200)  # More opaque for better visibility
        overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 72)  # Larger font for better visibility
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(self.width * CELL_SIZE // 2, self.height * CELL_SIZE // 2))
        screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption('RGB Minesweeper')
    clock = pygame.time.Clock()
    game = Minesweeper()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    if event.button == 1:  # Left click to reveal
                        game.reveal(grid_x, grid_y)
                    elif event.button == 3:  # Right click to flag
                        game.flag(grid_x, grid_y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Escape to end the game
                    game.game_over = True
                    game.reveal_all_mines()  # Reveal all mines

        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
