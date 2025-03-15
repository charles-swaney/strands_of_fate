from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Bard(Job):
    """
    A class entirely focused on buffing allies, and keeping morale high.

    Key Traits:
    - Very good charisma and luck growths.
    - Other growths are somewhat balanced across the board, with less
        emphasis on melee combat.
    - Has access to the widest range of ally buffing abilities in the game.

    Weapons:
    - Swords, Staves, Instruments

    Armor:
    - Light armor, Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 49
        return {
            "hp": 5,
            "mp": 7,
            "strength": 3,
            "toughness": 3,
            "dexterity": 5,
            "agility": 5,
            "intellect": 4,
            "wisdom": 4,
            "speed": 5,
            "tenacity": 3,
            "charisma": 9,
            "luck": 8
        }

    @property
    def class_aptitude(self) -> int:
        return 1

    @property
    def job_name(self) -> str:
        return "Bard"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["sword", "staff", "instrument"],
            "armor": ["light_armor", "robe"],
            "gauntlet": ["light_armor", "robe"],
            "greaves": ["light_armor", "robe"],
            "helmet": ["light_armor", "robe"],
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
