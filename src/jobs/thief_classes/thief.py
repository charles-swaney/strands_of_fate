from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Thief(Job):
    """
    An agile class with moderate growths in the speed/agility/dexterity
    departments. Focuses on curing/applying status effects and stealing
    from the enemy.

    Key Traits:
    - Decent growth in agility, dexterity, speed.
    - Weak defenses.
    - Has abilities to cure/apply status effects.
    - Has abilities to steal items from enemies.

    Weapons:
    - Swords, Daggers

    Armor:
    - Light armor
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 47
        return {
            "hp": 5,
            "mp": 4,
            "strength": 5,
            "toughness": 3,
            "dexterity": 7,
            "agility": 7,
            "intellect": 3,
            "wisdom": 2,
            "speed": 7,
            "tenacity": 3,
            "charisma": 4,
            "luck": 6
        }
    
    @property
    def class_aptitude(self) -> int:
        return 0
    
    @property
    def job_name(self) -> str:
        return "Thief"
    
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
                class_aptitude=self.class_aptitude)
            
            adventurer.base_stats[stat] += growth_rate + (bonus_mult * stat_bonus)
