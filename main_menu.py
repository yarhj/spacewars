import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космические Баталии")

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

font_path = "font/PressStart2P-vaV7.ttf"
font_size = 28
font = pygame.font.Font(font_path, font_size)

STAR_COUNT = 700
stars = [
    {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)}
    for _ in range(STAR_COUNT)
]
STAR_SPEED = 3


def display_start_screen(screen, WIDTH, HEIGHT):
    title_text = font.render("Spacewar", True, WHITE)
    instruction_text = font.render("Нажмите SPACE чтобы начать", True, WHITE)
    screen.fill(BLACK)

    for star in stars:
        color = YELLOW if random.random() > 0.8 else WHITE
        pygame.draw.rect(screen, color, (star["x"], star["y"], 3, 3))

    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    for star in stars:
        star["y"] += STAR_SPEED
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

    screen.fill(BLACK)

    for star in stars:
        color = YELLOW if random.random() > 0.8 else WHITE
        pygame.draw.rect(screen, color, (star["x"], star["y"], 3, 3))

    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)


waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False

    display_start_screen(screen, WIDTH, HEIGHT)

from game import main
main()
