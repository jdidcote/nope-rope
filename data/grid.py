from typing import Tuple

import pygame

class Grid:
    def __init__(
            self,
            width: int,
            grid_size: int,
            grid_color: Tuple[int]
    ):
        self.width = width
        self.grid_size = grid_size
        self.border_dist = width - grid_size
        self.grid_color = grid_color

    def draw(self, win):
        for x in range(0, self.width, self.grid_size):
            for y in range(0, self.width, self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(win, self.grid_color, rect, 1)