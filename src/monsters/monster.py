from core.stats.attributes import Attributes
from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from abc import ABC, abstractmethod
from utils.bonus_growth_calculations import compute_stat_bonus


class Monster(ABC):

    def __init__(
            self,
            monster_species: str,
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

        self.initialize_base_stats()

        for _ in range(2, self.level + 1):
            self.level_up()

        self._stats.update_override(stat_overrides)

    @property
    def stats(self) -> Attributes:
        """Return the Attributes class containing the monster's stats."""
        return self._stats

    @property
    def hp(self) -> float:
        """Return the monster's hp."""
        return self._stats.get_stat("hp")

    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        """Return the growth rate of each stat for this species."""
        pass

    @property
    @abstractmethod
    def elemental_resistances(self) -> ElementalResistances:
        """Return elemental resistances (e.g., fire, ice)."""
        pass

    @property
    @abstractmethod
    def weapon_resistances(self) -> WeaponResistances:
        """Return resistances to various weapon types (e.g., slashing, piercing)."""
        pass

    @property
    @abstractmethod
    def species_name(self) -> str:
        """Return the name of the monster."""
        pass

    @property
    @abstractmethod
    def class_aptitude(self) -> float:
        """Return the monster's aptitude."""
        pass

    @abstractmethod
    def get_element_res(self, element: str) -> float:
        """Return the monster's resistance to element."""
        pass

    @abstractmethod
    def get_weapon_res(self, weapon_type: str) -> float:
        """Return the monster's resistance to weapon_type."""
        pass

    def level_up(self):
        """Increase Monster level and apply stat growths."""
        self.level += 1
        self.apply_level_up()

    def initialize_base_stats(self):
        """Apply level up without incrementing level."""
        self.apply_level_up()

    def apply_level_up(self) -> None:
        """Level up the monster, based on growth rates and aptitude."""
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
            if growth_rate <= 3:
                bonus_mult = 0.5
            elif growth_rate >= 4 and growth_rate <= 8:
                bonus_mult = 1.0
            else:
                bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=self.aptitude,
                class_aptitude=self.class_aptitude
            )
            self.stats.add_to_stat(stat, growth_rate + (bonus_mult * stat_bonus))
