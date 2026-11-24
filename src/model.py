"""Параметры игры, ракетка, шарик, кирпичи и правила взаимодействия."""

import math
from dataclasses import dataclass


WINDOW_SIZE = (480, 640)  # Размер игрового поля в пикселях.
TARGET_FPS = 60  # Максимальная частота отрисовки.
MAX_FRAME_TIME = 0.05  # Максимальный шаг движения при задержке окна.
PADDLE_SPEED = 420  # Скорость ракетки в пикселях в секунду.
BALL_SPEED = 300  # Скорость шарика в пикселях в секунду.
BALL_LAUNCH_ANGLE = -70  # Угол запуска относительно оси X в градусах.
PADDLE_BOUNCE_ANGLE = 60  # Максимальный угол отскока от вертикали.
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
    """Хранить состояние поля и рассчитывать движение и столкновения."""

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
            # Малые шаги не дают шарику пролетать сквозь тонкие кирпичи.
            distance = math.hypot(self.ball.vx, self.ball.vy) * elapsed
            steps = max(1, math.ceil(distance / (self.ball.radius / 2)))
            for _ in range(steps):
                self.ball.x += self.ball.vx * elapsed / steps
                self.ball.y += self.ball.vy * elapsed / steps
                self._bounce_walls()
                self._bounce_paddle()
                self._hit_brick()

    def _bounce_walls(self):
        """Отразить шарик от боковых стен и потолка."""
        ball = self.ball
        if ball.x < ball.radius:
            ball.x = ball.radius
            ball.vx = abs(ball.vx)
        elif ball.x > WINDOW_SIZE[0] - ball.radius:
            ball.x = WINDOW_SIZE[0] - ball.radius
            ball.vx = -abs(ball.vx)
        if ball.y < ball.radius:
            ball.y = ball.radius
            ball.vy = abs(ball.vy)

    def _bounce_paddle(self):
        """Отбить падающий шарик, учитывая место попадания в ракетку."""
        ball = self.ball
        paddle = self.paddle
        if ball.vy <= 0 or ball.y > paddle.y:
            return
        if self._contact(paddle) is None:
            return
        # У центра отскок вертикальный, у краёв — под углом до 60°.
        offset = (ball.x - paddle.x - paddle.width / 2) / (paddle.width / 2)
        angle = math.radians(max(-1, min(1, offset)) * PADDLE_BOUNCE_ANGLE)
        speed = math.hypot(ball.vx, ball.vy)
        ball.vx = speed * math.sin(angle)
        ball.vy = -speed * math.cos(angle)
        ball.y = paddle.y - ball.radius

    def _contact(self, rectangle):
        """Вернуть нормаль и глубину пересечения круга с прямоугольником."""
        ball = self.ball
        closest_x = max(rectangle.x, min(ball.x, rectangle.x + rectangle.width))
        closest_y = max(rectangle.y, min(ball.y, rectangle.y + rectangle.height))
        dx, dy = ball.x - closest_x, ball.y - closest_y
        distance = math.hypot(dx, dy)
        if distance > ball.radius:
            return None
        if distance > 0:
            return dx / distance, dy / distance, ball.radius - distance
        # Если центр внутри блока, вытолкнуть его через ближайшую грань.
        edges = (
            (ball.x - rectangle.x, -1, 0),
            (rectangle.x + rectangle.width - ball.x, 1, 0),
            (ball.y - rectangle.y, 0, -1),
            (rectangle.y + rectangle.height - ball.y, 0, 1),
        )
        depth, nx, ny = min(edges, key=lambda edge: edge[0])
        return nx, ny, ball.radius + depth

    def _hit_brick(self):
        """Разрушить задетый кирпич и отразить шарик от его поверхности."""
        ball = self.ball
        for index, brick in enumerate(self.bricks):
            contact = self._contact(brick)
            if contact is None:
                continue
            nx, ny, depth = contact
            ball.x += nx * (depth + 0.001)
            ball.y += ny * (depth + 0.001)
            # Отражение v' = v - 2(v·n)n сохраняет модуль скорости.
            projection = ball.vx * nx + ball.vy * ny
            if projection < 0:
                ball.vx -= 2 * projection * nx
                ball.vy -= 2 * projection * ny
            self.bricks.pop(index)
            break
