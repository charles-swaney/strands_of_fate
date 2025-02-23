from abc import ABC, abstractmethod
from core.stats.attributes import Attributes
from enum import Enum, auto


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
            max_stacks: int = 1,
            scaling: float = 1.0):
        """
        A status effect class. Typically, these take on the form of either adding to or
        decreasing a unit's stats for a set number of turns. Status effects have a base
        magnitude which scales with the level of the caster. 

        Attributes:
            - name: the name of the status effect.
            - status_type: either a buff, debuff, or neutral
            - duration: how many turns the status effect lasts
            - magnitude: the base strength of the status effect
            - stacks: the number of stacks the status effect has been applied (e.g., Atk Up twice)
            - max_stacks: the maximum number of times the status effect can stack
            - scaling: the (multiplicative) extend to which the caster's level affects spell
                strength
        """
        self.name = name
        self._status_type = status_type
        self.duration = duration
        self.magnitude = magnitude
        self.stacks = stacks
        self._max_stacks = max_stacks
        self.scaling = scaling
        self.stat_mods = Attributes()
    
    @property
    def status_type(self) -> str:
        return self._status_type

    @property
    def max_stacks(self) -> str:
        return self._max_stacks
    
    def calculate_strength(self, level: int) -> int:
        return int(self.magnitude * self.scaling * level)
    
    def get_level(self, level: int):
        magnitude = self.calculate_strength(level)
        self.update_stat_mods(magnitude)
    
    @abstractmethod
    def update_stat_mods(self, magnitude: int, *other_factors: float):
        """Must be implemented by each effect."""
        pass
