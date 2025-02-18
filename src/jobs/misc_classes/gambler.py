from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer


class Gambler(Job):
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 56
        return {
            "hp": 4,
            "mp": 6,
            "strength": 3,
            "toughness": 3,
            "dexterity": 8,
            "agility": 9,
            "intellect": 2,
            "wisdom": 4,
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
            adventurer.base_stats[stat] += growth_rate + (bonus_mult * stat_bonus)
