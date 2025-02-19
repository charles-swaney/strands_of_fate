from abc import ABC, abstractmethod
from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances


class MonsterSpecies(ABC):
    """
    Base class defining general properties of a monster like resistances.
    """

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
    def species_name(self) -> float:
        """Return the name of the monster."""
        pass

    @property
    @abstractmethod
    def class_aptitude(self) -> float:
        """Return the monster's aptitude."""
        pass

    @property
    @abstractmethod
    def apply_level_up(self) -> None:
        """Level up the monster, based on growth rates and aptitude."""
        pass
