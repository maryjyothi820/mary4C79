import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Circle Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)

# Circle properties
RADIUS = 30
circle_pos = (random.randint(RADIUS, WIDTH - RADIUS), random.randint(RADIUS, HEIGHT - RADIUS))

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            cx, cy = circle_pos
            # Check if click is inside the circle
            if (mx - cx)**2 + (my - cy)**2 <= RADIUS**2:
                score += 1
                circle_pos = (random.randint(RADIUS, WIDTH - RADIUS), random.randint(RADIUS, HEIGHT - RADIUS))
    
    # Draw circle
    pygame.draw.circle(screen, BLUE, circle_pos, RADIUS)
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

