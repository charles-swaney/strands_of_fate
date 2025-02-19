from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Ronin(Job):
    """
    Describe the Ronin class.

    Key Traits:
    - Incredible strength growth, and solid growths in agility, dexterity, and speed.
    - Very high single-target damage.
    - Weak defenses, lack of supporting and ranged abilities.

    Weapons:
    - Sword, Katana

    Armor:
    - Light armor
    """

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 53
        return {
            "hp": 6,
            "mp": 3,
            "strength": 10,
            "toughness": 4,
            "dexterity": 6,
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
        return 1

    @property
    def job_name(self) -> str:
        return "Ronin"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["sword", "katana"],
            "armor": ["light_armor"],
            "gauntlet": ["light_armor"],
            "greaves": ["light_armor"],
            "helmet": ["light_armor"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "strength": 175,
            "dexterity": 100,
            "agility": 100
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Fighter": 10
        })

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
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
