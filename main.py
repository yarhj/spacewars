import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 450, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические Баталии")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

STAR_COUNT = 200
stars = [
    {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)}
    for _ in range(STAR_COUNT)
]

STAR_SPEED = 2


class Ship:
    def __init__(self, image_path, scale, speed):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)


ship = Ship("sprites/ship.png", (60, 60), 5)


class Laser:    # добавить урон
    def __init__(self, x, y, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 5
        self.color = color

    def move(self):
        self.rect.y -= self.speed if self.color == (0, 255, 0) else -self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Enemy:    # летят у верха не пропадут пока не умрут
    def __init__(self, image_path, scale, speed):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed
        self.direction = random.choice([-1, 1])
        self.move_counter = 0
        self.last_shot_time = pygame.time.get_ticks()

    def move(self):
        self.rect.y += self.speed
        self.move_counter += 1
        if self.move_counter % 60 == 0:
            self.direction = random.choice([-1, 1])
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 3000:
            enemy_lasers.append(Laser(self.rect.centerx, self.rect.bottom, (255, 0, 0)))
            self.last_shot_time = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)


enemies = [Enemy("sprites/enemies.png", (60, 50), 2) for _ in range(random.randint(1, 2))]
enemy_lasers = []


def spawn_enemy():
    for _ in range(random.randint(1, 3)):
        enemies.append(Enemy("sprites/enemies.png", (60, 50), 2))


ENEMY_SPAWN_TIME = 3000

last_enemy_spawn_time = pygame.time.get_ticks()

lasers = []
last_shot_time = pygame.time.get_ticks()


def shoot_laser():
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time > 400:
        lasers.append(Laser(ship.rect.centerx, ship.rect.top))
        last_shot_time = current_time


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        shoot_laser()

    current_time = pygame.time.get_ticks()  # поменять спавн
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_TIME:
        spawn_enemy()
        last_enemy_spawn_time = current_time

    for star in stars:
        star["y"] += STAR_SPEED
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

    ship.move(keys)

    for enemy in enemies:
        enemy.move()
        enemy.shoot()

    screen.fill(BLACK)
    for star in stars:
        color = YELLOW if random.random() > 0.8 else WHITE
        pygame.draw.rect(screen, color, (star["x"], star["y"], 3, 3))

    for laser in lasers[:]:
        laser.move()
        if laser.rect.bottom < 0:
            lasers.remove(laser)

    for enemy_laser in enemy_lasers[:]:
        enemy_laser.move()
        if enemy_laser.rect.top > HEIGHT:
            enemy_lasers.remove(enemy_laser)

    for laser in lasers:
        laser.draw(screen)

    for enemy_laser in enemy_lasers:
        enemy_laser.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    ship.draw(screen)

    pygame.display.flip()
    clock.tick(60)
