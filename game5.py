import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 500
ROWS, COLS = 8, 6
BLOCK_SIZE = 50
FPS = 60
POP_DELAY = 400

COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
]

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Blocks Pop - Continuous Play")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)

def create_grid():
    return [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

grid = create_grid()

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            if color:
                pygame.draw.rect(screen, color,
                                 (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

def draw_text(text, x, y, font_obj=None, color=TEXT_COLOR):
    if font_obj is None:
        font_obj = font
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

def move_left(temp_grid):
    new_grid = []
    for row in temp_grid:
        new_row = [c for c in row if c is not None]
        new_row += [None] * (COLS - len(new_row))
        new_grid.append(new_row)
    return new_grid

def move_right(temp_grid):
    new_grid = []
    for row in temp_grid:
        new_row = [c for c in row if c is not None]
        new_row = [None] * (COLS - len(new_row)) + new_row
        new_grid.append(new_row)
    return new_grid

def pop_same_color(temp_grid):
    to_pop = [[False] * COLS for _ in range(ROWS)]
    popped_any = False

    for row in range(ROWS):
        count = 1
        for col in range(1, COLS):
            if temp_grid[row][col] is not None and temp_grid[row][col] == temp_grid[row][col - 1]:
                count += 1
            else:
                if count >= 2:
                    popped_any = True
                    for c in range(col - count, col):
                        to_pop[row][c] = True
                count = 1
        if count >= 2:
            popped_any = True
            for c in range(COLS - count, COLS):
                to_pop[row][c] = True

    for row in range(ROWS):
        for col in range(COLS):
            if to_pop[row][col]:
                temp_grid[row][col] = None

    return popped_any, temp_grid

def drop_blocks(temp_grid):
    for col in range(COLS):
        col_blocks = [temp_grid[row][col] for row in range(ROWS) if temp_grid[row][col] is not None]
        for row in reversed(range(ROWS)):
            if col_blocks:
                temp_grid[row][col] = col_blocks.pop()
            else:
                temp_grid[row][col] = None
    return temp_grid

def refill_grid(temp_grid):
    for row in range(ROWS):
        for col in range(COLS):
            if temp_grid[row][col] is None:
                temp_grid[row][col] = random.choice(COLORS)
    return temp_grid

def can_pop_after_move(direction):
    temp_grid = [row[:] for row in grid]
    if direction == "left":
        temp_grid = move_left(temp_grid)
    elif direction == "right":
        temp_grid = move_right(temp_grid)
    popped, _ = pop_same_color(temp_grid)
    return popped

def game_step(direction):
    global grid
    if direction == "left":
        grid = move_left(grid)
    elif direction == "right":
        grid = move_right(grid)

    popped = True
    while popped:
        popped, grid = pop_same_color(grid)
        if popped:
            draw_grid()
            pygame.display.flip()
            pygame.time.delay(POP_DELAY)
            grid = drop_blocks(grid)

    grid = refill_grid(grid)

def main():
    running = True

    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_pop_after_move("left"):
                        game_step("left")
                elif event.key == pygame.K_RIGHT:
                    if can_pop_after_move("right"):
                        game_step("right")

        draw_grid()
        draw_text("Use LEFT/RIGHT arrows to move blocks", 10, HEIGHT - 40)
        draw_text("Pop 2+ adjacent horizontal blocks", 10, HEIGHT - 20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
