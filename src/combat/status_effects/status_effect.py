from abc import ABC, abstractmethod
from core.stats.attributes import Attributes
from typing import Union, TYPE_CHECKING
from math import prod
from enum import Enum, auto

if TYPE_CHECKING:
    from adventurers.adventurer import Adventurer
    from monsters.monster import Monster


class StatusType(Enum):
    BUFF = auto()
    DEBUFF = auto()
    NEUTRAL = auto()


class StatusEffect(ABC):
    def __init__(
            self,
            name: str,
            status_type: StatusType,
            duration: int,
            magnitude: int,
            stacks: int = 1,
            max_stacks: int = 1):
        """
        A status effect class. Typically, these take the form of either adding to or
        decreasing a unit's stats for a set number of turns. Status effects have a base
        magnitude which scales with the level of the caster. 

        Attributes:
            - name: the name of the status effect.
            - status_type: either a buff, debuff, or neutral
            - duration: how many turns the status effect lasts
            - magnitude: the base strength of the status effect (typically interacts with
                Intellect)
            - stacks: the number of stacks the status effect has been applied (e.g., Atk Up twice)
            - max_stacks: the maximum number of times the status effect can stack
        """
        self.name = name
        self._status_type = status_type
        self.duration = duration
        self.magnitude = magnitude
        self.stacks = stacks
        self._max_stacks = max_stacks
        self.stat_mods = Attributes()
    
    @property
    def status_type(self) -> str:
        return self._status_type

    @property
    def max_stacks(self) -> str:
        return self._max_stacks
    
    def base_strength(self, caster: Union["Adventurer", "Monster"], *other_factors) -> float:
        if isinstance(self.status_type, StatusType.DEBUFF):
            extra_mult = prod(other_factors) if other_factors else 1.0
            strength = 0.40 * caster.get_total_stat("intellect") * extra_mult
        elif isinstance(self.status_type, StatusType.BUFF):
            extra_mult = prod(other_factors) if other_factors else 1.0
            strength = 0.50 * caster.get_total_stat("charisma") * extra_mult
        else:
            strength = 0
        return strength
    
    @abstractmethod
    def calculate_strength(self, caster: Union["Adventurer", "Monster"], *scaling_factors) -> int:
        pass
    
    @abstractmethod
    def stat_mods(self, magnitude: int, *other_factors) -> Attributes:
        """Must be implemented by each effect."""
        pass

    def tick(self) -> bool:
        """Tick the status effect for one turn."""
        self.duration -= 1
        return self.duration > 0
    
    def add_stack(self) -> bool:
        """Add a stack of the effect, if possible."""
        if self.stacks < self.max_stacks:
            self.stacks += 1
            return True
        return False
    
    def apply_to(self, target: Union["Adventurer", "Monster"]) -> None:
        target._status_effects.append(self)

    
