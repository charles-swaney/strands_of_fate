from abc import ABC, abstractmethod
from typing import Union, Optional
from monsters.monster import Monster
from adventurers.adventurer import Adventurer


class Action(ABC):
    """A class representing the actions a unit can take."""
    def __init__(self, name: str, cost_type: str, cost: int, target_type: str, cooldown: int):
        self.name = name
        self.cost_type = cost_type
        self.cost = cost
        self.target_type = target_type
        self._cooldown = cooldown

    @abstractmethod
    def cast(self, caster: Union[Adventurer, Monster], target: Union[Adventurer, Monster]) -> None:
        """Defines how the spell or ability is cast or performed."""
        pass

    @abstractmethod
    def can_be_cast(self) -> bool:
        """Returns True if caster can currently cast spell."""
        pass
    
    @abstractmethod
    def tick_cooldown(self) -> None:
        pass
