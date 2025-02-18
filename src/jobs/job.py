from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from jobs.job_requirements import JobLevelRequirement, StatRequirement
    from src.adventurers.adventurer import Adventurer
    from src.core.stats.attributes import Attributes


class Job(ABC):
    """
    Base class for Job.
    """
    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        """Return the growth rates for each stat."""
        pass

    @property
    @abstractmethod
    def job_name(self) -> str:
        """Return job name."""
        pass

    @property
    @abstractmethod
    def class_aptitude(self) -> int:
        """Return class aptitude."""
        pass

    @abstractmethod
    def apply_level_up(self, adventurer: "Adventurer") -> None:
        """Level up adventurer, increase stats, log in levels_added."""
        pass

    @abstractmethod
    def job_level_requirements(self) -> "JobLevelRequirement":
        "Return the job level requirements for this class."
        pass

    @abstractmethod
    def stats_requirements(self) -> "StatRequirement":
        "Return the stats requirements for this class."
        pass