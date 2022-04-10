from dataclasses import dataclass

from data.direction import Direction


@dataclass
class Position:
    x: int
    y: int

    def get_border(self, border_dist):
        """ If the current position is at a border return true
        """
        if self.x == 0:
            return Direction.left
        elif self.y == 0:
            return Direction.up
        elif self.x == border_dist:
            return Direction.right
        elif self.y == border_dist:
            return Direction.right
        else:
            return None

