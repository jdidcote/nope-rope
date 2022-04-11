from dataclasses import dataclass
from typing import List


@dataclass
class Direction:
    left = (-1, 0)
    right = (1, 0)
    up = (0, 1)
    down = (0, -1)

@dataclass
class OrthogonalDirections:
    orthogonal_directions = {
        Direction.left: [Direction.up, Direction.down],
        Direction.right: [Direction.up, Direction.down],
        Direction.up: [Direction.left, Direction.right],
        Direction.down: [Direction.left, Direction.right],
        None: [Direction.up, Direction.down, Direction.left, Direction.right]
    }
