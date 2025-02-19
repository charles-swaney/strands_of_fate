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
        for _ in range(self.level):
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
    def base_watk(self) -> float:
        """Damage dealt when attacking with a weapon."""
        base = (1.0 * self.total_stats.get_stat("strength") +
                0.03 * self.total_stats.get_stat("luck"))
        equipment_watk = sum(
            eq.watk for eq in self.equipment.slots.values() if eq is not None
            )
        return base + equipment_watk

    @property
    def base_wdef(self) -> float:
        """Resistance to physical damage."""
        base = (1.0 * self.total_stats.get_stat("toughness") +
                0.03 * self.total_stats.get_stat("luck"))
        equipment_wdef = sum(
            eq.wdef for eq in self.equipment.slots.values() if eq is not None
        )
        return base + equipment_wdef

    @property
    def base_matk(self) -> float:
        """Damage dealt with spells."""
        base = (1.0 * self.total_stats.get_stat("intellect") +
                0.15 * self.total_stats.get_stat("charisma") +
                0.03 * self.total_stats.get_stat("luck"))
        equipment_matk = sum(
            eq.matk for eq in self.equipment.slots.values() if eq is not None
        )
        return base + equipment_matk

    @property
    def base_mdef(self) -> float:
        """Resistence to magical damage."""
        base = (self.total_stats.get_stat("wisdom") +
                0.15 * self.total_stats.get_stat("tenacity") +
                0.03 * self.total_stats.get_stat("luck"))
        equipment_mdef = sum(
            eq.mdef for eq in self.equipment.slots.values() if eq is not None
        )
        return base + equipment_mdef

    def equip(self, slot, item: Equipment):
        """Equip the given item in slot and update stats."""
        self.equipment.equip(slot, item, self.job)

    def unequip(self, slot: str):
        """Unequip whatever is equipped in slot and update stats."""
        self.equipment.unequip(slot)

    def _add_level_gained(self) -> None:
        """Log a level up within the Adventurer's current class."""
        self.levels_gained[self.job.job_name] += 1

    def level_up(self):
        """Increase Adventurer level with stat growths and log level gained."""
        self.level += 1
        self.job.apply_level_up(self)
        self._add_level_gained()
