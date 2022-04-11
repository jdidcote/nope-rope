import pygame

from data.direction import Direction, OrthogonalDirections
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
        new_snake_direction = Direction.up
    elif keys_pressed[pygame.K_RIGHT]:
        new_snake_direction = Direction.right
    elif keys_pressed[pygame.K_DOWN]:
        new_snake_direction = Direction.down
    elif keys_pressed[pygame.K_LEFT]:
        new_snake_direction = Direction.left
    else: new_snake_direction = snake.current_direction

    allowed_directions = OrthogonalDirections.orthogonal_directions[snake.current_direction]

    # Only allow for orthogonal changes in direction
    if new_snake_direction in allowed_directions:
        snake.change_direction(new_snake_direction)


def handle_snake_movement(grid: Grid, snake: Snake):
    """ If the snake reaches the edge of the screen return
        the coordinates of the opposite side
    """
    snake_head_pos = snake.pos[-1]

    snake_border_last = snake.last_head_pos.get_border(grid.border_dist)

    # Dictionary of current direction to a tuple that maps to the opposite side of the screen
    def _flip_border_position(direction: Direction, pos: Position):
        """ Flip the snakes position if it crosses the border
        """
        x, y, = pos.x, pos.y
        new_pos = {
            x < 0: Position(grid.border_dist, y),
            x > grid.width: Position(0, y),
            y < 0: Position(x, grid.border_dist),
            y > grid.width: Position(x, 0)
        }
        return new_pos[True]

    try:
        snake.change_head_pos(_flip_border_position(snake_border_last, snake_head_pos))
    except KeyError:
        snake.move()

    # if snake_border_last is not None:
    #     snake.change_head_pos(_get_new_pos(snake_border_last, snake_head_pos))
    # else:
    #     snake.move()


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
