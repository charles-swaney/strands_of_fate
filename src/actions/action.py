from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING
from monsters.monster import Monster
from adventurers.adventurer import Adventurer

if TYPE_CHECKING:
    from adventurers.adventurer import Adventurer
    from monsters.monster import Monster


class Action(ABC):
    """A class representing the actions a unit can take."""
    def __init__(self, name: str, cost_type: str, base_cost: int, cost_scaling: float, target_type: str, cooldown: int):
        self.name = name
        self.cost_type = cost_type
        self.base_cost = base_cost
        self.cost_scaling = cost_scaling
        self.target_type = target_type
        self._cooldown = cooldown

    @abstractmethod
    def execute(self, caster: Union[Adventurer, Monster], target: Union[Adventurer, Monster]) -> None:
        """Defines how the spell or ability is cast or performed."""
        pass

    @abstractmethod
    def can_be_used(self) -> bool:
        """Returns True if caster can currently cast spell."""
        pass
    
    @abstractmethod
    def tick_cooldown(self) -> None:
        pass
