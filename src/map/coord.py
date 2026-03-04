from typing import Iterable

@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

def manhattan(a: Coord, b: Coord) -> int:
    """Compute the horizontal Manhattan distance between a and b."""
    return abs(a.x - b.x) + abs(a.y - b.y)

def coords_within_radius(center: Coord, radius: int) -> Iterable[Coord]:
    """Return all coordinates within radius radius of center."""
    for dx in range(-r, r + 1):
        remaining = radius - abs(dx)
        for dy in range(-remaining, remaining + 1):
            yield Coord(center.x + dx, center.y + dy, center.z) # center.z is a placeholder, need to figure out what to do with z coord
