import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Shape colors
SHAPE_COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, ORANGE]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.get_new_shape()
        self.next_shape = self.get_new_shape()
        self.score = 0
        self.game_over = False

    def get_new_shape(self):
        shape = random.choice(SHAPES)
        color = random.choice(SHAPE_COLORS)
        return {'shape': shape, 'color': color, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_shape(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, shape['color'], ((shape['x'] + x) * BLOCK_SIZE, (shape['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.screen, WHITE, ((shape['x'] + x) * BLOCK_SIZE, (shape['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


    def draw_next_shape(self):
        for y, row in enumerate(self.next_shape['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.next_shape['color'], ((SCREEN_WIDTH // BLOCK_SIZE + x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                        pygame.draw.rect(self.screen, WHITE, ((SCREEN_WIDTH // BLOCK_SIZE + x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    def check_collision(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if (shape['x'] + x < 0 or shape['x'] + x >= SCREEN_WIDTH // BLOCK_SIZE or
                        shape['y'] + y >= SCREEN_HEIGHT // BLOCK_SIZE or
                        self.grid[shape['y'] + y][shape['x'] + x] != BLACK):
                        return True
        return False

    def lock_shape(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[shape['y'] + y][shape['x'] + x] = shape['color']
        self.clear_lines()

    def clear_lines(self):
        lines_cleared = 0
        for y in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def rotate_shape(self, shape):
        rotated_shape = {'shape': [list(row) for row in zip(*shape['shape'][::-1])], 'color': shape['color'], 'x': shape['x'], 'y': shape['y']}
        if not self.check_collision(rotated_shape):
            return rotated_shape
        return shape

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_shape(self.current_shape)
            self.draw_shape(self.next_shape)
            self.draw_next_shape()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_shape['x'] -= 1
                        if self.check_collision(self.current_shape):
                            self.current_shape['x'] += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_shape['x'] += 1
                        if self.check_collision(self.current_shape):
                            self.current_shape['x'] -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_shape['y'] += 1
                        if self.check_collision(self.current_shape):
                            self.current_shape['y'] -= 1
                    elif event.key == pygame.K_UP:
                        self.current_shape = self.rotate_shape(self.current_shape)

            self.current_shape['y'] += 1
            if self.check_collision(self.current_shape):
                self.current_shape['y'] -= 1
                self.lock_shape(self.current_shape)
                self.current_shape = self.next_shape
                self.next_shape = self.get_new_shape()
                if self.check_collision(self.current_shape):
                    self.game_over = True

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()