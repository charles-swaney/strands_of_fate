from core.stats.attributes import Attributes
from typing import TYPE_CHECKING, Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from monsters.monster_species import MonsterSpecies


class Monster(ABC):

    def __init__(
            self,
            monster_species: "MonsterSpecies",
            level: int = 1,
            aptitude: float = 5,
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
        self.apply_level_up(self)

    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        """Return the growth rate of each stat for this species."""
        pass

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return elemental resistances (e.g., fire, ice)."""
        pass

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return resistances to various weapon types (e.g., slashing, piercing)."""
        pass

    @property
    def species_name(self) -> float:
        """Return the name of the monster."""
        pass

    @property
    def class_aptitude(self) -> float:
        """Return the monster's aptitude."""
        pass

    def apply_level_up(self) -> None:
        """Level up the monster, based on growth rates and aptitude."""
        pass
