from ursina import *

app = Ursina()

TILE_SIZE = 1
MAP = [
    "WWWWWWWWWW",
    "W        W",
    "W   G    W",
    "W        W",
    "WWWWWWWWWW",
]

player = Entity(model='cube', color=color.azure, scale=0.5, origin_y=-0.5, z=0, collider='box')
player.speed = 5

walls = []
goal = None

for y, row in enumerate(reversed(MAP)):
    for x, tile in enumerate(row):
        pos = (x * TILE_SIZE - (len(MAP[0]) * TILE_SIZE / 2) + TILE_SIZE / 2,
               y * TILE_SIZE - (len(MAP) * TILE_SIZE / 2) + TILE_SIZE / 2,
               0)
        if tile == "W":
            walls.append(Entity(model='cube', color=color.gray, scale=TILE_SIZE, position=pos, collider='box'))
        elif tile == "G":
            goal = Entity(model='cube', color=color.green, scale=0.8, position=pos, collider='box')

player.position = (0, -1, 0)

win_text = Text("", scale=5, origin=(0, 0), color=color.orange, enabled=False)

def update():
    if not player.enabled:
        return

    prev_x = player.x
    prev_y = player.y

    player.x += (held_keys['d'] - held_keys['a']) * time.dt * player.speed
    for wall in walls:
        if player.intersects(wall).hit:
            player.x = prev_x

    player.y += (held_keys['w'] - held_keys['s']) * time.dt * player.speed
    for wall in walls:
        if player.intersects(wall).hit:
            player.y = prev_y

    if goal and player.intersects(goal).hit:
        player.enabled = False
        win_text.text = "YOU WIN!"
        win_text.enabled = True

app.run()