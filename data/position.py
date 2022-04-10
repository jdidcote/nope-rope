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


def position_collision(pos1: Position, pos2: Position, tol: int) -> bool:
    """ Detects if two positions are colliding within a certain tolerance

    :param pos1: First Position object
    :param pos2: Second Position object
    :param tol: Tolerance in x/y to consider a collision
    :return: whether objects have collided
    """

    return (abs(pos1.x - pos2.x) < tol) and (abs(pos1.y - pos2.y) < tol)