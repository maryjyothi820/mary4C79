from ursina import *

app = Ursina()

my_cube = Entity(model='cube', color=color.white, position=(0, 0, 0), collider='box')
my_sphere = Entity(model='sphere', color=color.yellow, position=(2, 0, 0), collider='sphere')
my_cone = Entity(model='cone', color=color.orange, position=(-2, 0, 0), collider='mesh')

def input(key):
    # If the input is a keyboard key (exclude mouse buttons)
    if len(key) == 1 or key.isalpha() or key.isdigit() or key in ['space', 'enter', 'tab', 'backspace', 'escape']:
        my_cube.color = color.random_color()

    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=100)
        if hit_info.hit:
            hit_info.entity.color = color.random_color()

app.run()

