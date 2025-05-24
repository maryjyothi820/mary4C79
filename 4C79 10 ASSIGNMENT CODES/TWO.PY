import pygame, random, time
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)

keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
names = {k: kname for k, kname in zip(keys, ["UP", "DOWN", "LEFT", "RIGHT"])}

state, target, start = "wait", None, 0
msg = "Press SPACE to start"

run = True
while run:
    screen.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        if e.type == pygame.KEYDOWN:
            if state == "wait" and e.key == pygame.K_SPACE:
                pygame.time.set_timer(pygame.USEREVENT, random.randint(1000, 4000))
                msg, state = "Get Ready...", "delay"
            elif state == "show" and e.key == target:
                msg = f"Reaction: {time.time() - start:.3f}s! Press SPACE"
                state = "done"
            elif state == "show":
                msg = "Wrong key! Press SPACE"
                state = "done"
            elif state == "done" and e.key == pygame.K_SPACE:
                msg, state = "Press SPACE to start", "wait"
        if e.type == pygame.USEREVENT and state == "delay":
            pygame.time.set_timer(pygame.USEREVENT, 0)
            target, start, state = random.choice(keys), time.time(), "show"

    if state == "show":
        text = font.render(names[target], True, (255, 255, 255))
    else:
        text = font.render(msg, True, (255, 255, 255))

    screen.blit(text, text.get_rect(center=(400, 300)))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()