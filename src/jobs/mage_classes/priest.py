from jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Priest(Job):
    """
    An adventurer who has dedicated their life to the art of healing. Boast strong stat
    growths and access to a diverse array of healing and buffing spells.

    Key Traits:
    - Great stat growths.
    - Weak offensive capabilities.
    - Access to shields, rare for a mage class.

    Weapons:
    - Rods, Hammers, Staves

    Armor:
    - Robes

    Growths:
        "hp": 5,
        "mp": 7,
        "strength": 3,
        "toughness": 5,
        "dexterity": 5,
        "agility": 4,
        "intellect": 5,
        "wisdom": 9,
        "speed": 5,
        "tenacity": 7,
        "charisma": 6,
        "luck": 7
    """

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 56
        return {
            "hp": 5,
            "mp": 7,
            "strength": 3,
            "toughness": 5,
            "dexterity": 5,
            "agility": 4,
            "intellect": 5,
            "wisdom": 9,
            "speed": 5,
            "tenacity": 7,
            "charisma": 6,
            "luck": 7
        }

    @property
    def class_aptitude(self) -> int:
        return 2

    @property
    def job_name(self) -> str:
        return "Priest"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["rod", "staff", "hammer"],
            "armor": ["robe"],
            "gauntlet": ["robe"],
            "greaves": ["robe"],
            "helmet": ["robe"],
            "accessory": ["ring", "necklace"],
            "shield": ["shield"]
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "wisdom": 100,
            "tenacity": 50
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "WhiteMage": 15,
            "Knight": 5
        })

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
