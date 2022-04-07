from typing import List

from data.position import Position


class Snake:
    def __init__(self, pos: List[Position]):
        self.pos = pos
        self.current_direction = None

    def change_direction(self, direction: str):
        """Change the direction of the snake's movement
        """

        # Change the snakes current direction
        self.current_direction = direction

    def move(self, direction: str, velocity):
        """Add a new element to head of list in given direction
        """

        # If no direction currently set, don't move
        if self.current_direction is None:
            return

        if self.current_direction == "UP":
            self.pos[-1].y -= velocity

    def grow(self):
        """Add a new node to the start of the list and do nothing else
        """
        pass

    def reset(self):
        pass
