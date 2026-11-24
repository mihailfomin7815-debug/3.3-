"""Окно приложения, игровой цикл и обработка управления."""

import pygame

from .model import Game, MAX_FRAME_TIME, TARGET_FPS, WINDOW_SIZE
from .renderer import Renderer


def handle_event(event, game, renderer):
    """Обработать ввод и вернуть признак продолжения работы."""
    if event.type == pygame.QUIT:
        return False
    if event.type == pygame.KEYDOWN and not getattr(event, "repeat", False):
        if event.key == pygame.K_ESCAPE:
            game.paused = not game.paused
        elif event.key == pygame.K_r:
            game.restart()
        elif event.key == pygame.K_SPACE:
            game.launch()
    if event.type == pygame.MOUSEMOTION:
        game.move_paddle(event.pos[0])
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if game.paused:
            for action, rect in renderer.menu_buttons.items():
                if rect.collidepoint(event.pos):
                    if action == "exit":
                        return False
                    if action == "restart":
                        game.restart()
                    else:
                        game.paused = False
                    break
        else:
            game.launch()
    return True


def run():
    """Открыть окно, отрисовывать поле и завершить работу при закрытии."""
    pygame.init()
    try:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Арканоид")
        game = Game()
        renderer = Renderer(screen)
        clock = pygame.time.Clock()

        while True:
            elapsed = min(clock.tick(TARGET_FPS) / 1000, MAX_FRAME_TIME)
            for event in pygame.event.get():
                if not handle_event(event, game, renderer):
                    return
            keys = pygame.key.get_pressed()
            direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            game.update(elapsed, direction)
            renderer.draw(game)
            pygame.display.flip()
    finally:
        pygame.quit()
