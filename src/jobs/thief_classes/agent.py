from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Agent(Job):
    """
    An incredibly fast class, focusing on dealing consistent but low damage,
    and buffing allies' offense.

    Key Traits:
    - Amazing speed, dexterity, agility, charisma growth.
    - Very strong stat growths in general.
    - Abilities enhance ally damage and apply status effects.
    - Flexibility to equip ranged weapons.

    Weapons:
    - Swords, Daggers, Bows

    Armor:
    - Light armor, Robes

    Growths:
        "hp": 5,
        "mp": 5,
        "strength": 5,
        "toughness": 3,
        "dexterity": 8,
        "agility": 8,
        "intellect": 3,
        "wisdom": 3,
        "speed": 10,
        "tenacity": 3,
        "charisma": 7,
        "luck": 5
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 55
        return {
            "hp": 5,
            "mp": 5,
            "strength": 5,
            "toughness": 3,
            "dexterity": 8,
            "agility": 8,
            "intellect": 3,
            "wisdom": 3,
            "speed": 10,
            "tenacity": 3,
            "charisma": 7,
            "luck": 5
        }

    @property
    def class_aptitude(self) -> int:
        return -0.5

    @property
    def job_name(self) -> str:
        return "Agent"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["sword", "dagger", "bow"],
            "armor": ["light_armor", "robe"],
            "gauntlet": ["light_armor", "robe"],
            "greaves": ["light_armor", "robe"],
            "helmet": ["light_armor", "robe"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "dexterity": 120,
            "agility": 120,
            "speed": 80
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Thief": 15
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
