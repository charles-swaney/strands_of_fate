from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Archer(Job):
    """
    A class that focuses on dealing damage from afar.

    Key Traits:
    - Strong dexterity, decent growths across the board.
    - Low hp, toughness, tenacity, wisdom, lead to being quite squishy.
    - Focuses on dealing damage without taking damage, as well as targeting
        the enemy backline.

    Weapons:
    - Bows

    Armor:
    - Light armor

    Growths:
        "hp": 5,
        "mp": 3,
        "strength": 6,
        "toughness": 3,
        "dexterity": 8,
        "agility": 7,
        "intellect": 3,
        "wisdom": 3,
        "speed": 6,
        "tenacity": 3,
        "charisma": 5,
        "luck": 6
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 50
        return {
            "hp": 5,
            "mp": 3,
            "strength": 6,
            "toughness": 3,
            "dexterity": 8,
            "agility": 7,
            "intellect": 3,
            "wisdom": 3,
            "speed": 6,
            "tenacity": 3,
            "charisma": 5,
            "luck": 6
        }

    @property
    def class_aptitude(self) -> int:
        return -1

    @property
    def job_name(self) -> str:
        return "Archer"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["bow"],
            "armor": ["light_armor"],
            "gauntlet": ["light_armor"],
            "greaves": ["light_armor"],
            "helmet": ["light_armor"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({})

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({})

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
            if adventurer.deterministic:
                bonus_mult = 0
            else:
                if growth_rate <= 3:
                    bonus_mult = 0.5
                elif growth_rate >= 4 and growth_rate <= 8:
                    bonus_mult = 1
                else:
                    bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=adventurer.aptitude,
                class_aptitude=self.class_aptitude
                )
            adventurer.base_stats.add_to_stat(
                stat,
                growth_rate + (bonus_mult * stat_bonus)
            )
