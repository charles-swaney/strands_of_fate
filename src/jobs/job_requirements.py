from typing import Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from jobs.job import Job
    from src.adventurers.adventurer import Adventurer


class StatRequirement:
    def __init__(self, stat_reqs: Dict[str, int]):
        self.stat_reqs = stat_reqs
    
    def check(self, adventurer: "Adventurer") -> bool:
        return all(adventurer.base_stats.get(stat, 0) >= self.stat_reqs.get(stat, 0) for stat in self.stat_reqs)
    

class JobLevelRequirement:
    def __init__(self, job_level_reqs: Dict[str, int]):
        self.job_level_reqs = job_level_reqs

    def check(self, adventurer: "Adventurer") -> bool:
        return all(adventurer.levels_gained.get(job, 0) >= self.job_level_reqs.get(job, 0) for job in self.job_level_reqs)
