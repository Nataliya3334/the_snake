from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры
class GameObject:
    """
    Базовый класс для объектов игры.

    Атрибуты:
    position: Позиция на игровом поле(x, y)
    body_color: Цвет объекта в формате RGB
    """

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color
        """
        Инициализация объекта игры.
        """

    def draw(self):
        """Заглушка для отрисовки."""
        pass


class Apple(GameObject):
    """
    Класс для яблока в игре.

    Атрибуты:
    position: Позиция яблока на игровом поле
    body_color: Цвет яблока
    """

    def __init__(self, position=(0, 0)):
        super().__init__(position, body_color=(255, 0, 0))  # Красное яблоко

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Отрисовка яблока в рандомном месте поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        return True


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

    def __init__(self, position=(0, 0)):
        super().__init__(position, body_color=(0, 255, 0))  # Зелёная змейка
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сброс состояния змейки для начала новой игры."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def move(self, apple):
        """Движение змейки. Обновляет позицию змеи, проверяет столкновения."""
        new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                    self.positions[0][1] + self.direction[1] * GRID_SIZE)

        if new_head in self.positions:
            self.reset()

        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        self.positions = [new_head] + self.positions[:-1]

        if new_head == apple.position:
            self.length += 1
            self.positions.append(self.positions[-1])

            return True

        while apple.position in self.positions:
            apple.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

        return True

    def update_direction(self):
        """Обновление направления движения после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(self):
    """Обработка нажатия клавиш для изменения направления движения змеи."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():
    """Инициализация PyGame."""
    pygame.init()
    snake = Snake(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    apple = Apple(position=(
        randint(0, GRID_WIDTH - 1) * GRID_SIZE,
        randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    ))

    # Отрисовка головы змейки
    head_rect = pygame.Rect(snake.positions[0], (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, snake.body_color, head_rect)
    pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    if snake.positions[-1]:
        last_rect = pygame.Rect(snake.positions[-1], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    while True:
        clock.tick(20)

        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)

        # Основная логика игры.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
