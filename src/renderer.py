"""Отрисовка игрового поля, объектов, счётчиков и меню."""

import pygame

from .model import BRICK_HEIGHT, BRICK_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH


BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (235, 235, 235)
BORDER_COLOR = (104, 104, 104)
BRICK_TOP_COLOR = (255, 100, 100)
BRICK_BOTTOM_COLOR = (185, 15, 25)
PADDLE_TOP_COLOR = (246, 246, 246)
PADDLE_BOTTOM_COLOR = (125, 125, 125)
BALL_COLOR = (40, 110, 255)


class Renderer:
    """Подготовить изображения объектов и отрисовывать игровое поле."""

    def __init__(self, screen):
        """Сохранить окно и создать изображения кирпича и ракетки."""
        self.screen = screen
        self.font = pygame.font.SysFont("arial,dejavusans", 21)
        hint_font = pygame.font.SysFont("arial,dejavusans", 16)
        self.launch_hint = hint_font.render(
            "Пробел или щелчок — запуск", True, TEXT_COLOR
        )
        self.controls_hint = hint_font.render(
            "Esc — пауза    R — рестарт", True, TEXT_COLOR
        )
        self.menu_rect = pygame.Rect(0, 0, 300, 290)
        self.menu_rect.center = screen.get_rect().center
        self.menu_title = self.font.render("Пауза", True, TEXT_COLOR)
        self.menu_buttons = {}
        self.menu_labels = {}
        for index, (action, title) in enumerate((
            ("resume", "Продолжить"),
            ("restart", "Рестарт"),
            ("exit", "Выход"),
        )):
            self.menu_buttons[action] = pygame.Rect(
                self.menu_rect.left + 25,
                self.menu_rect.top + 70 + index * 60, 250, 44,
            )
            self.menu_labels[action] = self.font.render(
                title, True, TEXT_COLOR
            )
        self.menu_shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.menu_shade.fill((0, 0, 0, 175))
        self.brick_sprite = self._make_block(
            (BRICK_WIDTH, BRICK_HEIGHT),
            BRICK_TOP_COLOR, BRICK_BOTTOM_COLOR,
        )
        self.paddle_sprite = self._make_block(
            (PADDLE_WIDTH, PADDLE_HEIGHT),
            PADDLE_TOP_COLOR, PADDLE_BOTTOM_COLOR,
        )

    def draw(self, game):
        """Нарисовать кирпичи, ракетку, шарик и начальные счётчики."""
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(
            self.screen, (190, 190, 190), self.screen.get_rect(), width=1
        )
        for brick in game.bricks:
            self.screen.blit(
                self.brick_sprite, (round(brick.x), round(brick.y))
            )
        self.screen.blit(
            self.paddle_sprite, (round(game.paddle.x), round(game.paddle.y))
        )
        center = (round(game.ball.x), round(game.ball.y))
        pygame.draw.circle(
            self.screen, (20, 50, 145), center, game.ball.radius
        )
        pygame.draw.circle(
            self.screen, BALL_COLOR, center, game.ball.radius - 1
        )
        pygame.draw.circle(
            self.screen, (175, 215, 255),
            (center[0] - 2, center[1] - 2), 2,
        )

        score = self.font.render(f"Очки: {game.score}", True, TEXT_COLOR)
        lives = self.font.render(f"Жизни: {game.lives}", True, TEXT_COLOR)
        self.screen.blit(score, (20, 20))
        self.screen.blit(lives, lives.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        ))
        hint = self.controls_hint if game.launched else self.launch_hint
        self.screen.blit(hint, hint.get_rect(
            midbottom=(
                self.screen.get_width() // 2,
                self.screen.get_height() - 8,
            )
        ))
        if game.paused:
            self._draw_menu()

    def _draw_menu(self):
        """Нарисовать меню паузы и кнопки поверх игрового поля."""
        self.screen.blit(self.menu_shade, (0, 0))
        pygame.draw.rect(self.screen, (28, 28, 28), self.menu_rect)
        pygame.draw.rect(
            self.screen, BORDER_COLOR, self.menu_rect, width=1
        )
        self.screen.blit(self.menu_title, self.menu_title.get_rect(
            center=(self.menu_rect.centerx, self.menu_rect.top + 32)
        ))
        mouse = pygame.mouse.get_pos()
        for action, rect in self.menu_buttons.items():
            color = (85, 85, 85) if rect.collidepoint(mouse) else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            label = self.menu_labels[action]
            self.screen.blit(label, label.get_rect(center=rect.center))

    def _make_block(self, size, top_color, bottom_color):
        """Создать прямоугольный спрайт с градиентом и тёмной рамкой."""
        width, height = size
        sprite = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(
            sprite, BORDER_COLOR, sprite.get_rect(), border_radius=3
        )
        for y in range(1, height - 1):
            fraction = (y - 1) / (height - 3)
            color = tuple(
                round(top + (bottom - top) * fraction)
                for top, bottom in zip(top_color, bottom_color)
            )
            pygame.draw.line(sprite, color, (2, y), (width - 3, y))
        return sprite
