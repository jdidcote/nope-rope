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

pygame.font.init()
GAME_SCORE_FONT = pygame.font.SysFont("Arial", 80)
END_GAME_FONT = pygame.font.SysFont("Arial", 80)

INITIAL_SNAKE_POS = Position(
    HEIGHT // 2 - GRID_SIZE // 2,
    WIDTH // 2 - GRID_SIZE // 2
)
INITIAL_GAME_SPEED = 200
FOOD_SPEED_INCREASE = 5

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

    def _flip_border_position(pos: Position):
        """ Flip the snakes position if it crosses the border
        """
        x, y, = pos.x, pos.y
        safe_x = min(pos.x, grid.border_dist)
        safe_y = min(pos.y, grid.border_dist)

        flipped = False

        if x < 0:  # LEFT
            snake.change_head_pos(
                Position(grid.width, safe_y)
            )
            flipped = True
        if x > grid.width:  # RIGHT
            snake.change_head_pos(
                Position(0, safe_y)
            )
            flipped = True
        if y < 0:  # UP
            snake.change_head_pos(
                Position(safe_x, grid.width)
            )
            flipped = True
        if y > grid.width:  # DOWN
            snake.change_head_pos(
                Position(safe_x, 0)
            )
            flipped = True
        return flipped

    was_flipped = _flip_border_position(snake.pos[-1])

    if not was_flipped:
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
    is_game_over = False

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

        letter = GAME_SCORE_FONT.render(str(snake.current_score), 0, (149, 207, 207))
        WIN.blit(letter, (grid.grid_size // 2, grid.grid_size // 2))

        if (pygame.time.get_ticks() - last_movement_time > max(current_game_speed, 0)) and not is_game_over:
            last_movement_time = pygame.time.get_ticks()
            was_eaten = handle_food(snake, food, grid)
            handle_snake_movement(grid, snake)
            if was_eaten:
                current_game_speed -= FOOD_SPEED_INCREASE
                snake.current_score += 1
                food = Food(grid)

        # Check for game ending collision (head position duplicated in tail):
        if snake.pos[-1] in snake.pos[:-1]:
            game_over_text = END_GAME_FONT.render(str("Game over!"), 0, (0, 0, 0))
            WIN.blit(game_over_text, (0, grid.width // 2))
            is_game_over = True

        draw_snake(snake)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
