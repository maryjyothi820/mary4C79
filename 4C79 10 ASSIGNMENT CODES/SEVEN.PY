from ursina import *

app = Ursina()

ball = Entity(model='sphere', color=color.red, scale=0.5, position=(0, 0, 0), collider='sphere')
ball.vx, ball.vy = 5, 7
gravity = 15
bounce = 0.8

ground = Entity(model='cube', color=color.gray, scale=(10, 1, 1), position=(0, -5, 0), collider='box')
top_wall = Entity(model='cube', color=color.gray, scale=(10, 1, 1), position=(0, 5, 0), collider='box')
left_wall = Entity(model='cube', color=color.gray, scale=(1, 10, 1), position=(-5, 0, 0), collider='box')
right_wall = Entity(model='cube', color=color.gray, scale=(1, 10, 1), position=(5, 0, 0), collider='box')

def update():
    ball.vy -= gravity * time.dt
    ball.x += ball.vx * time.dt
    ball.y += ball.vy * time.dt

    if ball.intersects(ground).hit:
        ball.y = ground.y + ground.scale_y/2 + ball.scale_y/2
        ball.vy *= -bounce

    if ball.intersects(top_wall).hit:
        ball.y = top_wall.y - top_wall.scale_y/2 - ball.scale_y/2
        ball.vy *= -bounce

    if ball.intersects(left_wall).hit:
        ball.x = left_wall.x + left_wall.scale_x/2 + ball.scale_x/2
        ball.vx *= -1

    if ball.intersects(right_wall).hit:
        ball.x = right_wall.x - right_wall.scale_x/2 - ball.scale_x/2
        ball.vx *= -1

app.run()