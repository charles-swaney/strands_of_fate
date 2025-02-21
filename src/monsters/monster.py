from core.stats.attributes import Attributes
from typing import Dict, Optional
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from abc import ABC, abstractmethod
from utils.bonus_growth_calculations import compute_stat_bonus


class Monster(ABC):

    def __init__(
            self,
            level: int = 1,
            aptitude: float = 5,
            **stat_overrides: float):

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

    @property
    def base_watk(self) -> float:
        """
        Return the monster's base weapon attack. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        strength = self.get_total_stat("strength")
        luck = self.get_total_stat("luck")
        return (1.0 * strength + 0.03 * luck)

    @property
    def base_wdef(self) -> float:
        """
        Return the monster's base weapon defense. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        toughness = self.get_total_stat("toughness")
        luck = self.get_total_stat("luck")
        return (1.0 * toughness + 0.03 * luck)

    @property
    def base_matk(self) -> float:
        """
        Return the monster's base magic attack. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        intellect = self.get_total_stat("intellect")
        charisma = self.get_total_stat("charisma")
        luck = self.get_total_stat("luck")
        return (1.0 * intellect +
                0.15 * charisma +
                0.03 * luck)

    @property
    def base_mdef(self) -> float:
        """
        Return the monster's base magic defense. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        wisdom = self.get_total_stat("wisdom")
        tenacity = self.get_total_stat("tenacity")
        luck = self.get_total_stat("luck")
        return (1.0 * wisdom +
                0.15 * tenacity +
                0.03 * luck)

    @property
    @abstractmethod
    def watk(self) -> float:
        """Total weapon attack, including bonuses."""
        pass

    @property
    @abstractmethod
    def wdef(self) -> float:
        """Total weapon defense, including bonuses."""
        pass

    @property
    @abstractmethod
    def matk(self) -> float:
        """Total magic attack, including bonuses."""
        pass

    @property
    @abstractmethod
    def mdef(self) -> float:
        """Total magic defense, including bonuses."""
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

    def get_total_stat(self, stat: str) -> float:
        """Return stat."""
        return self.stats.get_stat(stat)

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
