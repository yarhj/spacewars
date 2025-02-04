import random
import sys

import pygame
from PIL import Image

from final_screen import draw_final_screen

pygame.init()

# Установка размеров окна
WIDTH, HEIGHT = 550, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические Войны")
font = pygame.font.Font("font/PressStart2P-vaV7.ttf", 18)

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Звезды
STAR_COUNT = 200
stars = [
    {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)}
    for _ in range(STAR_COUNT)
]

STAR_SPEED = 2

# Обработка гиф
gif_path = "sprites/explosion.gif"
gif = Image.open(gif_path)
frames = []

explosions = []

# Разбивка гиф на кадры
try:
    while True:
        frame = gif.convert("RGBA")
        frame_data = frame.tobytes()
        frame_size = frame.size
        pygame_frame = pygame.image.fromstring(frame_data, frame_size, "RGBA")
        frames.append(pygame_frame)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass


# Класс корабля
class Ship:
    def __init__(self, image_path, scale, speed, hp_image_path, max_hp):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = speed
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hp_image = pygame.image.load("sprites/hp.png")
        self.hp_image = pygame.transform.scale(self.hp_image, (30, 30))

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
        for i in range(self.current_hp):
            screen.blit(self.hp_image, (10 + i * 35, 10))

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0


# Класс лазера
class Laser:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 5
        self.color = color

    def move(self):
        self.rect.y -= self.speed if self.color == (0, 255, 0) else -self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# Класс врага
class Enemy:
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
        self.move_counter += 2
        if self.move_counter % 60 == 0:
            self.direction = random.choice([-1, 1])
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1400:
            enemy_lasers.append(Laser(self.rect.centerx, self.rect.bottom, (255, 0, 0)))
            self.last_shot_time = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Создание корабля игрока
ship = Ship("sprites/ship.png", (60, 60), 5, "sprites/hp.png", max_hp=3)

# Создание врагов
enemies = [Enemy("sprites/enemies.png", (60, 50), 2) for _ in range(1)]

enemy_lasers = []


# Функция спавна врагов
def spawn_enemy():
    for _ in range(random.randint(1, 2)):
        enemies.append(Enemy("sprites/enemies.png", (60, 50), 2))


ENEMY_SPAWN_TIME = 1750

last_enemy_spawn_time = pygame.time.get_ticks()

lasers = []
last_shot_time = pygame.time.get_ticks()

start_time = pygame.time.get_ticks()
score = 0


# Функция стрельбы лазером
def shoot_laser():
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time > 400:
        lasers.append(Laser(ship.rect.centerx, ship.rect.top))
        last_shot_time = current_time


# Функция перезапуска
def reset_game():
    global ship, enemies, enemy_lasers, lasers, score, start_time, running
    ship = Ship("sprites/ship.png", (60, 60), 5, "sprites/hp.png", max_hp=3)
    enemies = [Enemy("sprites/enemies.png", (60, 50), 2) for _ in range(1)]
    enemy_lasers = []
    lasers = []
    score = 0
    start_time = pygame.time.get_ticks()
    running = True


clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Проверка времени игры
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 900:
            lasers.append(Laser(ship.rect.centerx, ship.rect.top))
            last_shot_time = current_time

    # Спавн врагов
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_TIME:
        for _ in range(random.randint(1, 2)):
            enemies.append(Enemy("sprites/enemies.png", (60, 50), 2))
        last_enemy_spawn_time = current_time

    # Движение звезд
    for star in stars:
        star["y"] += STAR_SPEED
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

    # Движение корабля
    ship.move(keys)

    # Движение лазеров
    for laser in lasers[:]:
        laser.move()
        if laser.rect.bottom < 0:
            lasers.remove(laser)

    # Движение лазеров врагов
    for enemy_laser in enemy_lasers[:]:
        enemy_laser.move()

        if enemy_laser.rect.top > HEIGHT:
            enemy_lasers.remove(enemy_laser)

        elif enemy_laser.rect.colliderect(ship.rect):
            ship.take_damage(1)
            enemy_lasers.remove(enemy_laser)

    # Движение врагов и подсчет очков
    for enemy in enemies[:]:
        enemy.move()
        enemy.shoot()

        # Проверка высоты врага
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)
            continue
        # Проверка столкновения с врагом
        if ship.rect.colliderect(enemy.rect):
            ship.take_damage(1)
            enemies.remove(enemy)
            continue

        # Проверка столкновения лазера с врагом
        for laser in lasers[:]:
            if laser.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                lasers.remove(laser)
                score += 50
                # Создание взрыва на месте смерти врага
                explosions.append({
                    "frames": frames,
                    "index": 0,
                    "x": enemy.rect.centerx,
                    "y": enemy.rect.centery,
                    "timer": pygame.time.get_ticks()
                })
                break

    # Проверка хп
    if ship.current_hp <= 0:
        running = False
        if draw_final_screen(screen, score, font, WIDTH, HEIGHT, BLACK, WHITE):
            reset_game()
            continue

    # Отрисовка объектов на экране
    screen.fill(BLACK)
    for star in stars:
        color = YELLOW if random.random() > 0.8 else WHITE
        pygame.draw.rect(screen, color, (star["x"], star["y"], 3, 3))

    # Отрисовка объектов
    for laser in lasers:
        laser.draw(screen)

    for enemy_laser in enemy_lasers:
        enemy_laser.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for explosion in explosions[:]:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - explosion["timer"]

        # Скорость смены кадров
        frame_duration = 50
        frame_index = elapsed_time // frame_duration

        if frame_index < len(explosion["frames"]):
            # Отрисовываем текущий кадр взрыва
            frame = explosion["frames"][frame_index]
            screen.blit(frame, (explosion["x"] - frame.get_width() // 2, explosion["y"] - frame.get_height() // 2))
        else:
            # Удаляем взрыв
            explosions.remove(explosion)

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 50))

    # Отрисовка корабля
    ship.draw(screen)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)
