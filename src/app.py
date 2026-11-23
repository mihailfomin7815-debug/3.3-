"""Окно приложения, игровой цикл и обработка управления."""

import pygame

from .model import Game, TARGET_FPS, WINDOW_SIZE
from .renderer import Renderer


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
            clock.tick(TARGET_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            renderer.draw(game)
            pygame.display.flip()
    finally:
        pygame.quit()
