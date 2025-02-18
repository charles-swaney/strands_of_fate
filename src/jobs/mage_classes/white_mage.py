from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class WhiteMage(Job):
    """
    A mage class that focuses primarily on healing allies, and secondarily
    on buffing them.

    Key Traits:
    - Strong wisdom growth.
    - Reasonable toughness growth affords some tankiness, for a mage.
    - Access to a wide range of healing spells.

    Weapons:
    - Rods, Hammers

    Armor:
    - Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 43
        return {
            "hp": 4,
            "mp": 6,
            "strength": 3,
            "toughness": 5,
            "dexterity": 3,
            "agility": 4,
            "intellect": 5,
            "wisdom": 8,
            "speed": 3,
            "tenacity": 2,
            "charisma": 5,
            "luck": 5
        }
    
    @property
    def class_aptitude(self) -> int:
        return 1
    
    @property
    def job_name(self) -> str:
        return "WhiteMage"
    
    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({})
    
    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({})

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
