from abc import ABC, abstractmethod
from typing import Dict
from src.adventurers.adventurer import Adventurer


class Job(ABC):
    """
    Base class for Job.
    """
    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        pass

    @property
    @abstractmethod
    def job_name(self) -> str:
        pass

    @property
    @abstractmethod
    def class_aptitude(self) -> int:
        pass

    @abstractmethod
    def apply_level_up(self, adventurer: Adventurer) -> None:
        pass