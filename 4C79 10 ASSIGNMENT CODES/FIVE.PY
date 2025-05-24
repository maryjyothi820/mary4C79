import pygame
import sys

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 48)

# Input screen to enter winning score
def get_win_score():
    input_text = ''
    while True:
        screen.fill((0, 0, 0))
        msg = small_font.render("Enter score to win:", True, (255, 255, 255))
        screen.blit(msg, msg.get_rect(center=(W//2, 200)))

        user_input = small_font.render(input_text, True, (0, 255, 0))
        screen.blit(user_input, user_input.get_rect(center=(W//2, 300)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(30)

win_score = get_win_score()

# Game objects
ball = pygame.Rect(W//2 - 10, H//2 - 10, 20, 20)
ball_speed = [5, 5]
p1 = pygame.Rect(50, H//2 - 50, 20, 100)
p2 = pygame.Rect(W - 70, H//2 - 50, 20, 100)
paddle_speed = 7
score1 = score2 = 0
game_over = False

def reset_ball():
    ball.center = (W//2, H//2)
    ball_speed[0] *= -1

# Main loop
while True:
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: p1.y = max(0, p1.y - paddle_speed)
        if keys[pygame.K_s]: p1.y = min(H - p1.height, p1.y + paddle_speed)
        if keys[pygame.K_UP]: p2.y = max(0, p2.y - paddle_speed)
        if keys[pygame.K_DOWN]: p2.y = min(H - p2.height, p2.y + paddle_speed)

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.top <= 0 or ball.bottom >= H:
            ball_speed[1] *= -1
        if ball.colliderect(p1) or ball.colliderect(p2):
            ball_speed[0] *= -1

        if ball.left <= 0:
            score2 += 1
            reset_ball()
        elif ball.right >= W:
            score1 += 1
            reset_ball()

        if score1 >= win_score or score2 >= win_score:
            game_over = True
            winner = "Player 1" if score1 >= win_score else "Player 2"

    pygame.draw.rect(screen, (255, 255, 255), p1)
    pygame.draw.rect(screen, (255, 255, 255), p2)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)

    score_text = font.render(f"{score1} : {score2}", True, (255, 255, 255))
    screen.blit(score_text, score_text.get_rect(center=(W//2, 30)))

    if game_over:
        win_text = small_font.render(f"{winner} Wins! Press ESC to quit.", True, (255, 255, 0))
        screen.blit(win_text, win_text.get_rect(center=(W//2, H//2)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()

    pygame.display.flip()
    clock.tick(60)