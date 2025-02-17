from typing import Optional, Dict, Union, TYPE_CHECKING
from collections import defaultdict
from src.equipment.armor import Armor
from src.equipment.weapon import Weapon

if TYPE_CHECKING:
    from src.jobs.job import Job

class Adventurer:
    
    def __init__(
        self,
        name: str,
        job: "Job",
        level: int = 0,
        levels_gained: Optional[Union[Dict[str, int], defaultdict]] = None,
        aptitude: float = 5,
        **stat_overrides: float):

        self.name = name
        self.job = job
        self.level = level
        self.levels_gained: defaultdict[str, int] = defaultdict(int)
        if isinstance(levels_gained, dict):
            self.levels_gained.update(levels_gained)
        elif isinstance(levels_gained, defaultdict):
            self.levels_gained = levels_gained.copy()
        self.aptitude = aptitude

        self.base_stats: Dict[str, float] = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "toughness": 0,
            "dexterity": 0,
            "agility": 0,
            "intellect": 0,
            "wisdom": 0,
            "speed": 0,
            "tenacity": 0,
            "charisma": 0,
            "luck": 0,
        }

        for stat, value in stat_overrides.items():
            if stat in self.base_stats:
                self.base_stats[stat] = value

        self.equipment: Dict[str, Optional[Union[Weapon, Armor]]] = {
            "weapon": Optional[Weapon],
            "armor": Optional[Armor],
            "gauntlet": Optional[Armor],
            "greaves": Optional[Armor],
            "helmet": Optional[Armor],
            "accessory": Optional[Armor],
            "shield": Optional[Armor],
        }

        self.job.apply_level_up(self)

    @property
    def base_watk(self) -> float:
        base = self.base_stats["strength"] + 0.03 * self.base_stats["luck"]
        bonus = 0
        for equipment in self.equipment.values():
            if equipment is not None:
                bonus += equipment.watk
        return base + bonus
    
    @property
    def base_wdef(self) -> float:
        base = self.base_stats["toughness"] + 0.03 * self.base_stats["luck"]
        bonus = 0
        for equipment in self.equipment.values():
            if equipment is not None:
                bonus += equipment.wdef
        return base + bonus
    
    @property
    def base_matk(self) -> float:
        base = (self.base_stats["intellect"] +
                0.15 * self.base_stats["charisma"] +
                0.03 * self.base_stats["luck"])
        bonus = 0
        for equipment in self.equipment.values():
            if equipment is not None:
                bonus += equipment.matk
        return base + bonus
    
    @property
    def base_mdef(self) -> float:
        base = (self.base_stats["wisdom"] +
                0.15 * self.base_stats["tenacity"] +
                0.03 * self.base_stats["luck"])
        bonus = 0
        for equipment in self.equipment.values():
            if equipment is not None:
                bonus += equipment.mdef
        return base + bonus

    def get_total_stats(self) -> None:
        total_stats = self.base_stats.copy()
        for item in self.equipment.values():
            if item:
                for stat, bonus in item.equipment_stat_bonuses.items():
                    total_stats[stat] += bonus
        return total_stats
    
    def _add_level_gained(self) -> None:
        self.levels_gained[self.job.job_name] += 1

    def level_up(self):
        self.level += 1
        self.job.apply_level_up(self)
        self._add_level_gained()