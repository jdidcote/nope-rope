from time import sleep

import pygame

from data.snake import Position, Snake

FPS = 60
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRID_SIZE = 20

INITIAL_SNAKE_POS = Position(
    HEIGHT // 2 - GRID_SIZE // 2,
    WIDTH // 2 - GRID_SIZE // 2
)

WHITE = (255, 255, 255)
BG_COLOUR = (217, 180, 178)
SNAKE_COLOR = (95, 130, 86)


class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def draw(self):
        for x in range(0, WIDTH, self.grid_size):
            for y in range(0, WIDTH, self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(WIN, WHITE, rect, 1)


def draw_snake(snake: Snake):
    for segment in snake.pos:
        segment_rect = pygame.Rect(segment.x, segment.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(WIN, SNAKE_COLOR, segment_rect)


def handle_snake_movement(snake: Snake, keys_pressed):
    if keys_pressed[pygame.K_UP]:  # UP
        snake.change_direction("UP")
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        snake.change_direction("RIGHT")
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        snake.change_direction("DOWN")
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        snake.change_direction("LEFT")


def main():
    clock = pygame.time.Clock()

    grid = Grid(GRID_SIZE)
    snake = Snake([INITIAL_SNAKE_POS])

    run = True
    while run:
        WIN.fill(BG_COLOUR)
        grid.draw()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        handle_snake_movement(snake, keys_pressed)

        # Current game speed in milliseconds since last snake movement
        current_game_speed = 500  # THIS WILL SCALE DOWN WITH CURRENT SNAKE LENGTH

        if snake.current_direction is None:
            # Define the last time the snake moved as 0
            last_movement_time = 0
        else:
            if pygame.time.get_ticks() - last_movement_time > current_game_speed:
                snake.move(GRID_SIZE)
                last_movement_time = pygame.time.get_ticks()



        draw_snake(snake)
        pygame.display.update()


    pygame.quit()


if __name__ == '__main__':
    main()
