from typing import Dict


class Attributes:
    def __init__(self, stats: Dict[str, float]):
        self.stats = stats.copy()

    def get_stat(self, stat_name: str) -> float:
        """Return the specified stat."""
        return self.stats.get(stat_name, 0)

    def items(self) -> Dict[str, float]:
        return self.stats.items()

    def add_to_stat(self, stat_name: str, value: float):
        """Add value to the specified stat."""
        self.stats[stat_name] = self.stats.get(stat_name, 0) + value

    def update_override(self, stat_overrides: Dict[str, float]):
        """Update stats with the given overrides."""
        for stat, value in stat_overrides.items():
            self.stats[stat] = value

    def copy(self) -> "Attributes":
        """Create a deep copy."""
        return Attributes(self.stats.copy())

    def update(self, other: "Attributes") -> "Attributes":
        """Add stats from other to current Attributes (e.g. equipping items)."""
        for stat, value in other.items():
            self.add_to_stat(stat, value)
        return self
