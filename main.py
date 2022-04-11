import pygame

from data.direction import Direction
from data.food import Food
from data.grid import Grid
from data.position import Position, position_collision
from data.snake import Snake
from logger import setup_logger

logger = setup_logger()

FPS = 30
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRID_SIZE = 20

INITIAL_SNAKE_POS = Position(
    HEIGHT // 2 - GRID_SIZE // 2,
    WIDTH // 2 - GRID_SIZE // 2
)
INITIAL_GAME_SPEED = 200
FOOD_SPEED_INCREASE = 50

WHITE = (255, 255, 255)
BG_COLOUR = (217, 180, 178)
SNAKE_COLOR = (95, 130, 86)


def draw_snake(snake: Snake):
    for segment in snake.pos:
        segment_rect = pygame.Rect(segment.x, segment.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(WIN, SNAKE_COLOR, segment_rect)


def handle_snake_direction(snake: Snake, keys_pressed):
    """ Control snake direction with user input
    """
    if keys_pressed[pygame.K_UP]:
        snake.change_direction(Direction.up)
    if keys_pressed[pygame.K_RIGHT]:
        snake.change_direction(Direction.right)
    if keys_pressed[pygame.K_DOWN]:
        snake.change_direction(Direction.down)
    if keys_pressed[pygame.K_LEFT]:
        snake.change_direction(Direction.left)


def handle_snake_movement(grid: Grid, snake: Snake):
    """ If the snake reaches the edge of the screen return
        the coordinates of the opposite side
    """
    snake_head_pos = snake.pos[-1]

    snake_border_last = snake.last_head_pos.get_border(grid.border_dist)
    snake_border = snake_head_pos.get_border(grid.border_dist)

    def _handle_borders():
        """ Handle the snake wrapping around the screen
        """
        if snake_border == Direction.up and snake.current_direction == Direction.up:
            new_pos = Position(snake_head_pos.x, grid.border_dist)
        elif snake_border == Direction.right and snake.current_direction == Direction.right:
            new_pos = Position(0, snake_head_pos.y)
        elif snake_border == Direction.down and snake.current_direction == Direction.down:
            new_pos = Position(snake_head_pos.x, 0)
        elif snake_border == Direction.left and snake.current_direction == Direction.left:
            new_pos = Position(grid.border_dist, snake_head_pos.y)
        else:
            new_pos = snake_head_pos

        snake.change_head_pos(new_pos)
    # If snake is at border and last position was not border, handle
    if (snake_border is not None) and (snake_border_last is None):
        _handle_borders()
    else:
        snake.move()


def handle_food(snake: Snake, food: Food, grid: Grid):
    is_eaten = position_collision(snake.pos[-1], food.pos, grid.grid_size // 2)
    if is_eaten:
        food.eaten = True
        snake.grow()
    return is_eaten


def main():
    clock = pygame.time.Clock()

    grid = Grid(WIDTH, GRID_SIZE, WHITE)
    snake = Snake(pos=[INITIAL_SNAKE_POS], step_size=GRID_SIZE)

    # Current game speed in milliseconds since last snake movement
    current_game_speed = INITIAL_GAME_SPEED
    last_movement_time = 0

    food = Food(grid)

    run = True
    while run:
        WIN.fill(WHITE)
        grid.draw(WIN)
        food.draw(WIN)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        handle_snake_direction(snake, keys_pressed)

        if pygame.time.get_ticks() - last_movement_time > current_game_speed:
            last_movement_time = pygame.time.get_ticks()
            was_eaten = handle_food(snake, food, grid)
            handle_snake_movement(grid, snake)
            if was_eaten:
                current_game_speed -= FOOD_SPEED_INCREASE
                food = Food(grid)

        draw_snake(snake)
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
