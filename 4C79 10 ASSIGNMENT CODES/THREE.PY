import pygame, random
pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

bucket = pygame.Rect(350, H - 50, 100, 50)
target_color = (0, 0, 255)  # Blue
score, blocks = 0, []

run = True
while run:
    screen.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  bucket.x = max(0, bucket.x - 7)
    if keys[pygame.K_RIGHT]: bucket.x = min(W - bucket.width, bucket.x + 7)

    if random.random() < 0.02:
        color = random.choice([(255, 0, 0), (0, 255, 0), target_color])
        rect = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
        blocks.append({'rect': rect, 'color': color, 'speed': random.randint(3, 7)})

    for b in blocks[:]:
        b['rect'].y += b['speed']
        if b['rect'].colliderect(bucket):
            if b['color'] == target_color: score += 1
            blocks.remove(b)
        elif b['rect'].y > H:
            blocks.remove(b)

    # Draw bucket
    pygame.draw.rect(screen, (100, 100, 100), bucket)

    # Draw falling blocks
    for b in blocks:
        pygame.draw.rect(screen, b['color'], b['rect'])

    # Display score
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

    # Display target color
    screen.blit(font.render("Catch this color:", True, (255, 255, 255)), (10, 50))
    pygame.draw.rect(screen, target_color, pygame.Rect(220, 50, 50, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()