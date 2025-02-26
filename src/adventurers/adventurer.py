from typing import Optional, Dict, Union, TYPE_CHECKING
from collections import defaultdict
from src.core.stats.attributes import Attributes
from equipment.equipment_slots import EquipmentSlots
from equipment.equipment import Equipment

if TYPE_CHECKING:
    from src.jobs.job import Job


class Adventurer:

    def __init__(
            self,
            name: str,
            job: "Job",
            level: int = 1,
            levels_gained: Optional[Union[Dict[str, int], defaultdict]] = None,
            aptitude: float = 5,
            deterministic: bool = False,
            **stat_overrides: float):

        self.name = name
        self.job = job
        self.level = level
        self.deterministic = deterministic
        self._status_effects = []
        self.levels_gained: defaultdict[str, int] = defaultdict(int)
        if isinstance(levels_gained, dict):
            self.levels_gained.update(levels_gained)
        elif isinstance(levels_gained, defaultdict):
            self.levels_gained = levels_gained.copy()
        self.aptitude = aptitude

        base_stats = {
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

        self._base_stats = Attributes(base_stats)

        self._equipment = EquipmentSlots(valid_slots=self.job.allowed_item_types)

        self.initialize_base_stats()

        for _ in range(2, self.level + 1):
            self.job.apply_level_up(self)
        self._base_stats.update_override(stat_overrides)

    @property
    def base_stats(self) -> Attributes:
        """Base stats without equipment or other bonuses."""
        return self._base_stats

    @property
    def equipment_bonuses(self) -> Attributes:
        """Stat bonuses from all equipment."""
        return self.equipment.get_equipment_bonuses()

    @property
    def total_stats(self) -> Attributes:
        """Total stats from base stats, equipment, and other bonuses."""
        total = self._base_stats.copy()
        return total.update(self.equipment_bonuses)

    @property
    def equipment(self) -> Equipment:
        return self._equipment
    
    @property
    def hp(self) -> float:
        """Return the (current) hp."""
        return self.total_stats.get_stat('hp')

    @property
    def watk(self) -> float:
        """Damage dealt when attacking with a weapon."""
        base = (1.0 * self.get_total_stat("strength") +
                0.03 * self.get_total_stat("luck"))
        equipment_watk = self.get_equipment_combat_stat('watk')
        return base + equipment_watk

    @property
    def wdef(self) -> float:
        """Resistance to physical damage."""
        base = (1.0 * self.get_total_stat("toughness") +
                0.03 * self.get_total_stat("luck"))
        equipment_wdef = self.get_equipment_combat_stat('wdef')
        return base + equipment_wdef

    @property
    def matk(self) -> float:
        """Damage dealt with spells."""
        base = (1.08 * self.get_total_stat("intellect") +
                0.03 * self.get_total_stat("luck"))
        equipment_matk = self.get_equipment_combat_stat('matk')
        return base + equipment_matk

    @property
    def mdef(self) -> float:
        """Resistence to magical damage."""
        base = (self.get_total_stat("wisdom") +
                0.15 * self.get_total_stat("tenacity") +
                0.03 * self.get_total_stat("luck"))
        equipment_mdef = self.get_equipment_combat_stat('mdef')
        return base + equipment_mdef
    
    def get_equipment_combat_stat(self, stat: str) -> float:
        """Return the total combat stat (e.g. matk, wdef) from all equipment."""
        stat_total = sum(
            getattr(equipment, stat) for equipment in self.equipment.slots.values() if
            equipment is not None
        )
        return stat_total

    def get_base_stat(self, stat: str) -> float:
        """Conveniently return the base stat."""
        return self.base_stats.get_stat(stat)

    def get_total_stat(self, stat: str) -> float:
        """Conveniently return the total stat."""
        return self.total_stats.get_stat(stat)

    def equip(self, slot, item: Equipment):
        """Equip the given item in slot and update stats."""
        self.equipment.equip(slot, item, self.job)

    def unequip(self, slot: str):
        """Unequip whatever is equipped in slot and update stats."""
        self.equipment.unequip(slot)

    def _add_level_gained(self) -> None:
        """Log a level up within the Adventurer's current class."""
        self.levels_gained[self.job.job_name] += 1

    def initialize_base_stats(self) -> None:
        """Initialize adventurer with base stats."""
        self.job.apply_level_up(self)

    def level_up(self):
        """Increase Adventurer level with stat growths and log level gained."""
        self.level += 1
        self.job.apply_level_up(self)
        self._add_level_gained()
