from core.stats.attributes import Attributes
from typing import Optional, Dict, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from monsters.monster_species import MonsterSpecies

class Monster:

    def __init__(
            self,
            monster_species: "MonsterSpecies",
            level: int=0,
            aptitude: float=5,
            **stat_overrides: float):

        self.monster_species = monster_species
        self.level = level
        self.aptitude = aptitude

        ZERO_STATS = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "toughness": 0,
            "dexterity": 0,
            "agility": 0,
            "intellect": 0,
            "wisdom": 0,
            "speed": 0,
            "tenacity": 0,
            "charisma": 0,
            "luck": 0,
        }

        self._stats = Attributes(ZERO_STATS)
                                      
        for _ in range(self.level):
            self.level_up()
        self._stats.update_override(stat_overrides)

    @property
    def stats(self) -> Attributes:
        return self._stats
    

    def level_up(self):
        """Increase Monster level with stat growths."""
        self.level += 1
        self.monster_species.apply_level_up(self)
