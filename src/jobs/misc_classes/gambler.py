from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Gambler(Job):
    """
    A class centered almost entirely around luck-based mechanics.

    Key Traits:
    - Incredible luck growth.
    - Extremely poor growth in magic-related skills, and extremely squishy overall.
    - Abilities range from damage-dealing, debuffing, and buffing allies,
        but always with a reliance random chance.

    Weapons:
    - Daggers

    Armor:
    - Light armor
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 52
        return {
            "hp": 4,
            "mp": 6,
            "strength": 3,
            "toughness": 3,
            "dexterity": 7,
            "agility": 8,
            "intellect": 2,
            "wisdom": 2,
            "speed": 7,
            "tenacity": 2,
            "charisma": 7,
            "luck": 11
        }
    
    @property
    def class_aptitude(self) -> int:
        return 0
    
    @property
    def job_name(self) -> str:
        return "Gambler"
    
    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "agility": 80,
            "luck": 150 # Only the lucky can gamble !
        })
    
    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Jester": 5,
            "Bard": 5
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
