from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Jester(Job):
    """
    A class focused on sowing chaos and discord on the battlefield.

    Key Traits:
    - Very strong speed, charisma, agility, luck growths.
    - Abilities focus on buffing allies and debuffing enemies.

    Weapons:
    - Daggers

    Armor:
    - Light armor
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 54
        return {
            "hp": 5,
            "mp": 4,
            "strength": 4,
            "toughness": 3,
            "dexterity": 6,
            "agility": 8,
            "intellect": 3,
            "wisdom": 4,
            "speed": 9,
            "tenacity": 1,
            "charisma": 9,
            "luck": 7
        }

    @property
    def class_aptitude(self) -> int:
        return 0

    @property
    def job_name(self) -> str:
        return "Jester"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["dagger"],
            "armor": ["light_armor"],
            "gauntlet": ["light_armor"],
            "greaves": ["light_armor"],
            "helmet": ["light_armor"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "agility": 100,
            "speed": 70,
            "charisma": 90
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Thief": 5
        })

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        base_growth_rates = self.growth_rates

        for stat, growth_rate in base_growth_rates.items():
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
