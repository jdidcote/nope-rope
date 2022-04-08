from typing import List

from data.position import Position


class Snake:
    def __init__(self, pos: List[Position], step_size: float):
        self.pos = pos
        self.current_direction = None
        self.step_size = step_size

        # Head and tail positions
        self.head_pos = self.pos[-1]
        self.tail_pos = self.pos[0]

    def change_direction(self, direction: str):
        """Change the direction of the snake's movement
        """

        # Change the snakes current direction
        self.current_direction = direction

    def move(self):
        """Add a new element to head of list in given direction
        """

        # If no direction currently set, don't move
        if self.current_direction is None:
            return

        self._move_head()

    def _move_head(self):

            if self.current_direction == "UP":
                self.pos[-1].y -= self.step_size
            if self.current_direction == "RIGHT":
                self.pos[-1].x += self.step_size
            if self.current_direction == "DOWN":
                self.pos[-1].y += self.step_size
            if self.current_direction == "LEFT":
                self.pos[-1].x -= self.step_size

    def grow(self):
        """Add a new node to the start of the list and do nothing else
        """
        pass

    def reset(self):
        pass
