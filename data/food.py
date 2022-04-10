import random

import pygame

from data.grid import Grid
from data.position import Position


class Food:
    def __init__(self, grid: Grid):
        self.eaten = False
        self.grid = grid
        self._set_random_position()

    def _set_random_position(self):
        space = list(range(0 + self.grid.grid_size // 4, self.grid.width, self.grid.grid_size))
        self.pos = Position(random.choice(space), random.choice(space))

    def draw(self, win):
        if self.eaten:
            rect = pygame.Rect(self.pos.x, self.pos.y, 0, 0)
        else:
            rect = pygame.Rect(self.pos.x, self.pos.y, self.grid.grid_size // 2, self.grid.grid_size // 2)
        pygame.draw.rect(win, (0, 0, 0), rect)
