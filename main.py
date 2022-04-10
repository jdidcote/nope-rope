import pygame

from data.direction import Direction
from data.snake import Position, Snake

FPS = 60
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRID_SIZE = 20

INITIAL_SNAKE_POS = Position(
    HEIGHT // 2 - GRID_SIZE // 2,
    WIDTH // 2 - GRID_SIZE // 2
)
INITIAL_GAME_SPEED = 250

WHITE = (255, 255, 255)
BG_COLOUR = (217, 180, 178)
SNAKE_COLOR = (95, 130, 86)


class Grid:
    def __init__(self, width: int, grid_size: int):
        self.width = width
        self.grid_size = grid_size
        self.border_dist = width - grid_size

    def draw(self):
        for x in range(0, WIDTH, self.grid_size):
            for y in range(0, WIDTH, self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(WIN, WHITE, rect, 1)


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
    # print(snake_border_last, snake_border)
    # print(snake.last_head_pos, snake_head_pos)

    def _handle_borders():
        """ Handle the snake wrapping around the screen
        """
        if snake_border == Direction.up and snake.current_direction == Direction.up:
            new_pos = Position(snake_head_pos.x, grid.border_dist)
        if snake_border == Direction.right and snake.current_direction == Direction.right:
            new_pos = Position(0, snake_head_pos.y)
        if snake_border == Direction.down and snake.current_direction == Direction.down:
            new_pos = Position(snake_head_pos.x, 0)
        if snake_border == Direction.left and snake.current_direction == Direction.left:
            new_pos = Position(grid.border_dist, snake_head_pos.y)
        snake.change_head_pos(new_pos)

    # If snake is at border and last position was not border, handle
    if (snake_border is not None) and (snake_border_last is None):
        _handle_borders()
    else:
        snake.move()


def main():
    clock = pygame.time.Clock()

    grid = Grid(WIDTH, GRID_SIZE)
    snake = Snake(pos=[INITIAL_SNAKE_POS], step_size=GRID_SIZE)

    run = True
    while run:
        WIN.fill(BG_COLOUR)
        grid.draw()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        handle_snake_direction(snake, keys_pressed)

        # Current game speed in milliseconds since last snake movement
        current_game_speed = INITIAL_GAME_SPEED  # THIS WILL SCALE DOWN WITH CURRENT SNAKE LENGTH

        if snake.current_direction is None:
            # Define the last time the snake moved as 0
            last_movement_time = 0
        else:
            if pygame.time.get_ticks() - last_movement_time > current_game_speed:
                handle_snake_movement(grid, snake)
                last_movement_time = pygame.time.get_ticks()

        draw_snake(snake)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
