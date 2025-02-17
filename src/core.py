from dataclasses import dataclass
from typing import Dict
from src.jobs.base import Job

@dataclass
class Adventurer:
    name: str
    job: Job
    level: int = 1
    levels_gained: Dict[str, int]

    # Combat Stats
    hp: float
    mp: float
    strength: float
    toughness: float
    dexterity: float
    agility: float
    intellect: float
    willpower: float

    watk: float
    wdef: float
    matk: float
    mdef: float

    # Auxiliary Stats
    tenacity: float
    charisma: float
    aptitude: float
    luck: float

    def level_up(self):
        self.level += 1
        self.job.on_level_up(self)