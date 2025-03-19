from jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Duelist(Job):
    """
    Describe the Duelist class.

    Key Traits:
    - Exceptional single-target damage, with a wide range of skills for bolstering prowess
        in single combat.
    - Excellent offensive stat growths, but poor hp and defensive stat growths.
    - Strong array of damage-dealing abilities.

    Weapons:
    - Swords, Katanas

    Armor:
    - Light armor

    Growths:
        "hp": 6,
        "mp": 2,
        "strength": 9,
        "toughness": 5,
        "dexterity": 8,
        "agility": 8,
        "intellect": 2,
        "wisdom": 2,
        "speed": 8,
        "tenacity": 3,
        "charisma": 5,
        "luck": 6
    """

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 54
        return {
            "hp": 6,
            "mp": 2,
            "strength": 9,
            "toughness": 5,
            "dexterity": 8,
            "agility": 8,
            "intellect": 2,
            "wisdom": 2,
            "speed": 8,
            "tenacity": 3,
            "charisma": 4,
            "luck": 5
        }

    @property
    def class_aptitude(self) -> int:
        return 1

    @property
    def job_name(self) -> str:
        return "Duelist"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["sword", "katana"],
            "armor": ["light_armor"],
            "gauntlet": ["light_armor",],
            "greaves": ["light_armor",],
            "helmet": ["light_armor",],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "strength": 100,
            "dexterity": 80,
            "agility": 80,
            "speed": 80,
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
                "Ronin": 10
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
