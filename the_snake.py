"""Простая игра Змейка с использованием Pygame."""
import pygame as pg
from random import randint, choice

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Описание классов игры
class GameObject:
    """
    Базовый класс для объектов игры.

    Атрибуты:
    position: Позиция на игровом поле(x, y)
    body_color: Цвет объекта в формате RGB
    border_color: Цвет границы ячейки
    """

    def __init__(
            self,
            position=None,
            body_color=None,
            border_color=BORDER_COLOR
    ):
        """Инициализация объекта игры."""
        self.position = position if position else CENTER_POSITION
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self, position):
        """Метод для отрисовки одной ячейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """Метод draw для автотестов."""
        self.draw_cell(self.position)


class Apple(GameObject):
    """
    Класс для яблока в игре.

    Атрибуты:
    position: Позиция яблока на игровом поле
    body_color: Цвет яблока
    """

    def __init__(
            self,
            position=None,
            body_color=None,
            border_color=BORDER_COLOR,
            occupied_positions=(CENTER_POSITION,)
    ):
        """Инициализация яблока."""
        # Устанавливаем цвет яблока по умолчанию
        if body_color is None:
            body_color = (255, 0, 0)  # Красное яблоко

        # Если позиция не указана, генерируем случайную
        if position is None:
            position = self.randomize_position(occupied_positions)

        super().__init__(position, body_color, border_color)

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в рандомное место, избегая занятых клеток."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                return new_position

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """
    Класс для змейки в игре.

    Атрибуты:
    positions: Список позиций всех сегментов тела змейки
    body_color: Цвет змейки
    length: Длина змейки
    direction: Направление движения змейки
    next_direction: Направление движения после нажатия клавиши
    """

    def __init__(
            self,
            position=None,
            body_color=None,
            border_color=BORDER_COLOR
    ):
        """Инициализация змейки."""
        # Устанавливаем позицию и цвет по умолчанию
        if position is None:
            position = CENTER_POSITION
        if body_color is None:
            body_color = (0, 255, 0)  # Зелёная змейка

        super().__init__(position, body_color, border_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки с учётом границ экрана."""
        head_x, head_y = self.positions[0]
        return (
            head_x % SCREEN_WIDTH,
            head_y % SCREEN_HEIGHT
        )

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            self.draw_cell(position)

    def reset(self):
        """Сброс состояния змейки для начала новой игры."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def move(self):
        """Движение змейки. Обновляет позицию змеи."""
        # Получаем координаты головы змейки с помощью распаковки
        head_x, head_y = self.get_head_position()

        # Вычисляем новые координаты головы
        new_head = (head_x + self.direction[0] * GRID_SIZE,
                    head_y + self.direction[1] * GRID_SIZE
                    )

        # Вставляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Удаляем последний сегмент
        return self.positions.pop()

    def check_self_collision(self):
        """Проверяет, столкнулась ли голова змейки с её телом."""
        return self.get_head_position() in self.positions[1:]

    def update_direction(self):
        """Обновление направления движения после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """Обработка нажатия клавиш для изменения направления движения змеи."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Инициализация PyGame."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        # Обработка нажатий клавиш
        handle_keys(snake)
        snake.update_direction()
        removed_tail = snake.move()

        # Проверка на столкновение с телом змейки
        if snake.check_self_collision():
            snake.reset()  # Сбрасываем состояние змейки при столкновении
            apple.randomize_position(snake.positions)
        else:
            # Проверка на поедание яблока
            if snake.get_head_position() == apple.position:
                snake.positions.append(removed_tail)
                snake.length += 1
                apple.randomize_position(snake.positions)

        # Основная логика игры
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
