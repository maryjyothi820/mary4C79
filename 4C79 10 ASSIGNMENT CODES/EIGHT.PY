from ursina import *

app = Ursina()

window.cursor = False  # Hide system cursor

# Define multiple cursor styles with their shape, color, and scale
cursor_styles = {
    '1': {'model': 'quad', 'color': color.red,    'scale': 0.03},
    '2': {'model': 'circle', 'color': color.green, 'scale': 0.02},
    '3': {'model': 'sphere', 'color': color.blue,  'scale': 0.04},
    '4': {'model': 'quad', 'color': color.yellow, 'scale': 0.05},
    '5': {'model': 'circle', 'color': color.orange, 'scale': 0.035},
}

# Start with cursor style 1
current_style_key = '1'

custom_cursor = Entity(
    parent=camera.ui,
    model=cursor_styles[current_style_key]['model'],
    color=cursor_styles[current_style_key]['color'],
    scale=cursor_styles[current_style_key]['scale'],
    always_on_top=True
)

typed_text = Text("", position=(-0.5, 0.4), scale=2, color=color.white)

def update():
    custom_cursor.position = mouse.position

def input(key):
    global current_style_key
    if key in cursor_styles:
        current_style_key = key
        style = cursor_styles[key]
        custom_cursor.model = style['model']
        custom_cursor.color = style['color']
        custom_cursor.scale = style['scale']
    elif key == 'backspace':
        typed_text.text = typed_text.text[:-1]
    elif key == 'escape':
        window.cursor = True
        quit()
    elif len(key) == 1:
     

   typed_text.text += key

app.run()
