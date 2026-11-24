"""Параметры игры, ракетка, шарик, кирпичи и правила взаимодействия."""

import math
from dataclasses import dataclass


WINDOW_SIZE = (480, 640)  # Размер игрового поля в пикселях.
TARGET_FPS = 60  # Максимальная частота отрисовки.
MAX_FRAME_TIME = 0.05  # Максимальный шаг движения при задержке окна.
PADDLE_SPEED = 420  # Скорость ракетки в пикселях в секунду.
BALL_SPEED = 300  # Скорость шарика в пикселях в секунду.
BALL_LAUNCH_ANGLE = -70  # Угол запуска относительно оси X в градусах.
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
    vx: float = 0.0
    vy: float = 0.0


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
        """Создать новую партию."""
        self.restart()

    def restart(self):
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
        self.launched = False
        self.paused = False

    def move_paddle(self, center_x):
        """Переместить центр ракетки, ограничив её границами поля."""
        if self.paused:
            return
        self.paddle.x = max(
            0.0,
            min(center_x - self.paddle.width / 2,
                WINDOW_SIZE[0] - self.paddle.width),
        )
        if not self.launched:
            self.ball.x = self.paddle.x + self.paddle.width / 2

    def launch(self):
        """Однократно запустить шарик с текущего положения над ракеткой."""
        if self.launched or self.paused:
            return
        angle = math.radians(BALL_LAUNCH_ANGLE)
        self.ball.vx = BALL_SPEED * math.cos(angle)
        self.ball.vy = BALL_SPEED * math.sin(angle)
        self.launched = True

    def update(self, elapsed, direction=0):
        """Переместить ракетку и запущенный шарик за прошедшее время."""
        if self.paused:
            return
        center = self.paddle.x + self.paddle.width / 2
        self.move_paddle(
            center + max(-1, min(1, direction)) * PADDLE_SPEED * elapsed
        )
        if self.launched:
            self.ball.x += self.ball.vx * elapsed
            self.ball.y += self.ball.vy * elapsed
