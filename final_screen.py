import sys

import pygame


def draw_final_screen(screen, score, font, WIDTH, HEIGHT, BLACK, WHITE):
    """
    Отрисовывает финальный экран с результатами игры.
    Возвращает True, если игрок нажал пробел для перезапуска игры.
    """
    screen.fill(BLACK)

    # Отображение текста "Game Over"
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Отображение количества очков
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)

    # Отображение текста "Нажмите SPACE Для Игры Снова"
    restart_text = font.render("Нажмите SPACE Для Игры Снова", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    # Ожидание нажатия пробела для перезапуска игры
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
    return False
