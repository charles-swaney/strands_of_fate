from abc import ABC, abstractmethod
from typing import Dict
from src.core import Adventurer


class Job(ABC):
    """
    Base class for Job.
    """
    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def on_level_up(self, adventurer: Adventurer) -> None:
        pass