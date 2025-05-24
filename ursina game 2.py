from ursina import *
import random

app = Ursina()

ROWS, COLS = 8, 6
BLOCK_SIZE = 1

COLORS = [color.red, color.green, color.blue, color.yellow, color.orange]

grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

def create_block(row, col):
    cube_color = random.choice(COLORS)
    block = Entity(
        model='cube',
        color=cube_color,
        position=(col * BLOCK_SIZE, -row * BLOCK_SIZE, 0),
        scale=BLOCK_SIZE * 0.9
    )
    return block

def create_grid():
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = create_block(r, c)

def move_left():
    for r in range(ROWS):
        row_blocks = [b for b in grid[r] if b is not None]
        for c in range(COLS):
            if c < len(row_blocks):
                grid[r][c] = row_blocks[c]
                grid[r][c].position = (c * BLOCK_SIZE, -r * BLOCK_SIZE, 0)
            else:
                if grid[r][c] is not None:
                    destroy(grid[r][c])
                grid[r][c] = None

def move_right():
    for r in range(ROWS):
        row_blocks = [b for b in grid[r] if b is not None]
        for c in range(COLS):
            pos = COLS - len(row_blocks) + c
            if c < len(row_blocks) and 0 <= pos < COLS:
                grid[r][pos] = row_blocks[c]
                grid[r][pos].position = (pos * BLOCK_SIZE, -r * BLOCK_SIZE, 0)
            else:
                if grid[r][c] is not None:
                    destroy(grid[r][c])
                grid[r][c] = None

def pop_adjacent():
    to_pop = [[False]*COLS for _ in range(ROWS)]
    popped_any = False

    for r in range(ROWS):
        count = 1
        for c in range(1, COLS):
            current = grid[r][c]
            prev = grid[r][c-1]
            if current and prev and current.color == prev.color:
                count += 1
            else:
                if count >= 2:
                    popped_any = True
                    for i in range(c - count, c):
                        to_pop[r][i] = True
                count = 1
        if count >= 2:
            popped_any = True
            for i in range(COLS - count, COLS):
                to_pop[r][i] = True

    for r in range(ROWS):
        for c in range(COLS):
            if to_pop[r][c] and grid[r][c]:
                destroy(grid[r][c])
                grid[r][c] = None

    return popped_any

def drop_blocks():
    for c in range(COLS):
        col_blocks = [grid[r][c] for r in range(ROWS) if grid[r][c] is not None]
        for r in reversed(range(ROWS)):
            idx = ROWS - 1 - r
            if idx < len(col_blocks):
                grid[r][c] = col_blocks[idx]
                grid[r][c].position = (c * BLOCK_SIZE, -r * BLOCK_SIZE, 0)
            else:
                if grid[r][c] is not None:
                    destroy(grid[r][c])
                grid[r][c] = None

def refill_grid():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] is None:
                grid[r][c] = create_block(r, c)

def game_step(direction):
    if direction == 'left':
        move_left()
    else:
        move_right()

    popped = True
    while popped:
        popped = pop_adjacent()
        if popped:
            drop_blocks()
            invoke(lambda: None, delay=0.2)

    refill_grid()

def input(key):
    if key == 'left':
        game_step('left')
    elif key == 'right':
        game_step('right')
        
create_grid()
camera.position = (COLS * BLOCK_SIZE / 2 - BLOCK_SIZE / 2, -ROWS * BLOCK_SIZE / 2 + BLOCK_SIZE / 2, -15)
camera.look_at(Vec3(COLS * BLOCK_SIZE / 2 - BLOCK_SIZE / 2, -ROWS * BLOCK_SIZE / 2 + BLOCK_SIZE / 2, 0))

app.run()

