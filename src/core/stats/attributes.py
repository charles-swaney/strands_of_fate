from typing import Dict


class Attributes:
    def __init__(self, stats: Dict[str, float]):
        self.stats = stats.copy()
    
    def get_stat(self, stat_name: str) -> float:
        return self.stats.get(stat_name, 0)
    
    def add_to_stat(self, stat_name: str, value: float):
        self.stats[stat_name] = self.stats.get(stat_name, 0) + value

    def update(self, stat_overrides: Dict[str, float]):
        """Update stats with the given overrides."""
        for stat, value in stat_overrides.items():
            self.stats[stat] = value

    def copy(self) -> "Attributes":
        """Create a deep copy."""
        return Attributes(self.stats.copy())
