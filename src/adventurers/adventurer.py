from typing import Optional, Dict, Union
from src.equipment.equipment import Equipment
from src.equipment.armor import Armor
from src.equipment.weapon import Weapon

class Adventurer:
    def __init__(
        self,
        name: str,
        job: "Job",
        level: int = 0,
        levels_gained: Optional[Dict[str, int]] = None,
        aptitude: float = 0,
        **stat_overrides: float
    ):
        self.name = name
        self.job = job
        self.level = level
        self.levels_gained = levels_gained or {}
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
            "tenacity": 0,
            "charisma": 0,
            "luck": 0,
        }

        for stat, value in stat_overrides.items():
            if stat in self.base_stats:
                self.base_stats[stat] = value

        self.equipment: Dict[str, Optional[Union[Weapon, Armor]]] = {
            "weapon": None,
            "armor": None,
            "gauntlet": None,
            "greaves": None,
            "helmet": None,
            "accessory": None,
            "shield": None,
        }

        self.job.apply_level_up(self)

    @property
    def base_watk(self) -> float:
        base = self.strength + 0.03 * self.luck
        weapon = self.equipment.get("weapon")
        return base + (weapon.damage if weapon else 0)
    
    @property
    def base_wdef(self) -> float:
        base = self.toughness + 0.03 * self.luck
        armor_defense = 0
        for equipment in self.equipment:
            if isinstance(equipment, Armor):
                armor_defense += equipment.wdef
        return base + armor_defense
    
    @property
    def base_matk(self) -> float:
        base = self.intellect + 0.15 * self.charisma + 0.03 * self.luck
        bonus = 0
        for equipment in self.equipment:
            bonus += equipment.stats.get("matk")
        return base + bonus
    
    @property
    def base_mdef(self) -> float:
        base = self.wisdom + 0.15 * self.tenacity + 0.03 * self.luck
        bonus = 0
        for equipment in self.equipment:
            bonus += equipment.stats.get("mdef")
        return base + bonus

    def get_total_stats(self) -> None:
        total_stats = self.base_stats.copy()
        for item in self.equipment.values():
            if item:
                for stat, bonus in item.equipment_stat_bonuses.items():
                    total_stats[stat] += bonus
        return total_stats


    def level_up(self):
        self.level += 1
        self.job.apply_level_up(self)