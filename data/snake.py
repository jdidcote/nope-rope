from copy import copy
from typing import List

from data.direction import Direction
from data.position import Position
from logger import setup_logger

logger = setup_logger()


class Snake:
    def __init__(self, pos: List[Position], step_size: float):
        self.pos = pos
        self.current_direction = None
        self.step_size = step_size
        self.last_head_pos = pos[-1]

    def change_direction(self, direction: str):
        """Change the direction of the snake's movement
        """

        # Change the snakes current direction
        self.current_direction = direction

    def _update_last_head_pos(self):
        self.last_head_pos = copy(self.pos[-1])

    def change_head_pos(self, new_head_pos: Position):
        """ Change the absolute position of the snake's head
        """
        self._update_last_head_pos()
        self.pos[-1] = new_head_pos

    def move(self):
        """Add a new element to head of list in given direction
        """

        # If no direction currently set, don't move
        if self.current_direction is None:
            return

        self._move_head()
        self._move_tail()

    def _move_head(self):
        """ Move the snake's head forward one step size
        """
        self._update_last_head_pos()

        if self.current_direction == Direction.up:
            self.pos[-1].y -= self.step_size
        if self.current_direction == Direction.right:
            self.pos[-1].x += self.step_size
        if self.current_direction == Direction.down:
            self.pos[-1].y += self.step_size
        if self.current_direction == Direction.left:
            self.pos[-1].x -= self.step_size

    def _move_tail(self):
        """ Move the snake's tail to the previous head position
        """
        if len(self.pos) > 1:
            del self.pos[0]
            self.pos.insert(-1, self.last_head_pos)

    def grow(self):
        """Add a new node to the start of the list and do nothing else
        """
        # Create a new position one square behind
        tail_pos = self.pos[0]
        new_position = Position(
            (tail_pos.x + (self.step_size * self.current_direction[0])),
            (tail_pos.y + (self.step_size * self.current_direction[0]))
        )

        self.pos = [new_position] + self.pos
        # logger.info(f"{self.pos}")

    def reset(self):
        pass
