"""Параметры игры, ракетка, шарик, кирпичи и правила взаимодействия."""

from dataclasses import dataclass


WINDOW_SIZE = (480, 640)  # Размер игрового поля в пикселях.
TARGET_FPS = 60  # Максимальная частота отрисовки.
PADDLE_WIDTH = 88  # Ширина ракетки в пикселях.
PADDLE_HEIGHT = 16  # Высота ракетки в пикселях.
PADDLE_BOTTOM_MARGIN = 40  # Расстояние от ракетки до нижнего края.
BALL_RADIUS = 8  # Радиус шарика в пикселях.
BALL_PADDLE_GAP = 3  # Зазор между шариком и ракеткой перед запуском.
BRICK_COLUMNS = 6  # Число кирпичей в строке.
BRICK_ROWS = 5  # Число строк кирпичей.
BRICK_WIDTH = 64  # Ширина кирпича в пикселях.
BRICK_HEIGHT = 18  # Высота кирпича в пикселях.
BRICK_GAP = 5  # Промежуток между кирпичами в пикселях.
BRICKS_TOP = 78  # Верхняя граница блока кирпичей в пикселях.
INITIAL_SCORE = 0  # Начальный счёт.
INITIAL_LIVES = 3  # Начальное число жизней.


@dataclass
class Paddle:
    """Хранить координаты верхнего левого угла и размеры ракетки."""

    x: float
    y: float
    width: int = PADDLE_WIDTH
    height: int = PADDLE_HEIGHT


@dataclass
class Ball:
    """Хранить координаты центра и радиус единственного шарика."""

    x: float
    y: float
    radius: int = BALL_RADIUS


@dataclass
class Brick:
    """Хранить координаты верхнего левого угла и размеры кирпича."""

    x: float
    y: float
    width: int = BRICK_WIDTH
    height: int = BRICK_HEIGHT


class Game:
    """Хранить начальное состояние игрового поля."""

    def __init__(self):
        """Расположить кирпичи, ракетку и шарик на игровом поле."""
        width, height = WINDOW_SIZE
        self.paddle = Paddle(
            (width - PADDLE_WIDTH) / 2,
            height - PADDLE_BOTTOM_MARGIN - PADDLE_HEIGHT,
        )
        self.ball = Ball(
            self.paddle.x + self.paddle.width / 2,
            self.paddle.y - BALL_RADIUS - BALL_PADDLE_GAP,
        )
        # Общая ширина сетки включает промежутки только между кирпичами.
        grid_width = BRICK_COLUMNS * BRICK_WIDTH
        grid_width += (BRICK_COLUMNS - 1) * BRICK_GAP
        left = (width - grid_width) / 2
        self.bricks = [
            Brick(
                left + column * (BRICK_WIDTH + BRICK_GAP),
                BRICKS_TOP + row * (BRICK_HEIGHT + BRICK_GAP),
            )
            for row in range(BRICK_ROWS)
            for column in range(BRICK_COLUMNS)
        ]
        self.score = INITIAL_SCORE
        self.lives = INITIAL_LIVES
