import pygame, random
pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- Sprites ---
class Player(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(W // 2, H - 30))
    def update(self, keys):
        if keys[pygame.K_LEFT]:  self.rect.x = max(0, self.rect.x - 7)
        if keys[pygame.K_RIGHT]: self.rect.x = min(W - self.rect.width, self.rect.x + 7)

class FallingObject(pygame.sprite.Sprite):
    def _init_(self, speed):
        super()._init_()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(random.randint(0, W - 30), 0))
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.kill()

# --- Game Setup ---
player = Player()
player_group = pygame.sprite.Group(player)
objects = pygame.sprite.Group()
lives, game_over, spawn_timer = 3, False, 0
level_speed = 4

# --- Game Loop ---
running = True
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False

    if not game_over:
        player.update(keys)

        if spawn_timer <= 0:
            level_speed += 0.01  # Gradually increase difficulty
            objects.add(FallingObject(int(level_speed)))
            spawn_timer = 20
        else:
            spawn_timer -= 1

        objects.update()

        if pygame.sprite.spritecollideany(player, objects):
            lives -= 1
            for obj in pygame.sprite.spritecollide(player, objects, True): pass
            if lives <= 0: game_over = True

    player_group.draw(screen)
    objects.draw(screen)

    screen.blit(font.render(f"Lives: {lives}", True, (255, 255, 255)), (10, 10))
    if game_over:
        msg = font.render("GAME OVER!", True, (255, 255, 255))
        screen.blit(msg, msg.get_rect(center=(W//2, H//2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()