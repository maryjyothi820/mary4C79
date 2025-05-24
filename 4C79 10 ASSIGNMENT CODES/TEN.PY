from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.blue, position=(0, -2, 0))

def change_player_color():
    player.color = color.random_color()

my_button = Button(
    text='Change Player Color',
    color=color.azure,
    highlight_color=color.lime,
    scale=(0.3, 0.1),
    position=(0, 0.3),
    on_click=change_player_color
)
app.run()