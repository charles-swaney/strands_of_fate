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

        self._base_stats: Dict[str, float] = {
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
            if stat in self._base_stats:
                self._base_stats[stat] = value

        self.equipment: Dict[str, Optional[Union[Weapon, Armor]]] = {
            "weapon": None,
            "armor": None,
            "gauntlet": None,
            "greaves": None,
            "helmet": None,
            "accessory": None,
            "shield": None,
        }

        self.job.apply_level_up(self) # Start at level 1

    @property
    def base_stats(self) -> Dict[str, float]:
        """Base stats without equipment or other bonuses."""
        return self._base_stats
    
    @property
    def equipment_bonuses(self) -> Dict[str, float]:
        """Stat bonuses from all equipment."""
        bonuses = defaultdict(float)
        for equipment in self.equipment.values():
            if equipment and hasattr(equipment, 'equipment_stat_bonuses'):
                for stat, value in equipment.equipment_stat_bonuses.items():
                    bonuses[stat] += value
        return bonuses

    @property
    def total_stats(self) -> Dict[str, float]:
        """Total stats from base stats, equipment, and other bonuses."""
        total = self._base_stats.copy()
        for stat, bonus in self.equipment_bonuses.items():
            total[stat] += bonus
        return total
    
    @property
    def base_watk(self) -> float:
        """Damage dealt when attacking with a weapon."""
        base = self.base_stats["strength"] + 0.03 * self.base_stats["luck"]
        equipment_watk = sum(
            eq.watk for eq in self.equipment.values() if eq is not None
            )
        stat_bonus = self.equipment_bonuses["strength"] + 0.03 * self.equipment_bonuses["luck"]
        return base + equipment_watk + stat_bonus
    
    @property
    def base_wdef(self) -> float:
        """Resistance to physical damage."""
        base = self.base_stats["toughness"] + 0.03 * self.base_stats["luck"]
        equipment_wdef = sum(
            eq.wdef for eq in self.equipment.values() if eq is not None
        )
        stat_bonus = self.equipment_bonuses["toughness"] + 0.03 * self.equipment_bonuses["luck"]
        return base + equipment_wdef + stat_bonus
    
    @property
    def base_matk(self) -> float:
        """Damage dealt with spells."""
        base = (self.base_stats["intellect"] +
                0.15 * self.base_stats["charisma"] +
                0.03 * self.base_stats["luck"])
        equipment_matk = sum(
            eq.matk for eq in self.equipment.values() if eq is not None
        )
        stat_bonus = (self.equipment_bonuses["intellect"] +
                      0.15 * self.equipment_bonuses["charisma"] +
                      0.03 * self.equipment_bonuses["luck"])
        return base + equipment_matk + stat_bonus
    
    @property
    def base_mdef(self) -> float:
        """Resistence to magical damage."""
        base = (self.base_stats["wisdom"] +
                0.15 * self.base_stats["tenacity"] +
                0.03 * self.base_stats["luck"])
        equipment_mdef = sum(
            eq.mdef for eq in self.equipment.values() if eq is not None
        )
        stat_bonus = (self.equipment_bonuses["wisdom"] +
                      self.equipment_bonuses["tenacity"] +
                      self.equipment_bonuses["luck"])
        return base + equipment_mdef + stat_bonus
    
    def _add_level_gained(self) -> None:
        """Log a level up within the Adventurer's current class."""
        self.levels_gained[self.job.job_name] += 1

    def level_up(self):
        """Increase Adventurer level with stat growths and log level gained."""
        self.level += 1
        self.job.apply_level_up(self)
        self._add_level_gained()