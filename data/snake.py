from typing import List

from data.position import Position


class Snake:
    def __init__(self, pos: List[Position]):
        self.pos = pos

    def move(self):
        """Add a new element to head of list in given direction
        """
        pass

    def grow(self):
        """Add a new node to the start of the list and do nothing else
        """

    def reset(self):
        pass
