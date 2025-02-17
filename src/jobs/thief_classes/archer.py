from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer


class Archer(Job):
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 50
        return {
            "hp": 5,
            "mp": 3,
            "strength": 6,
            "toughness": 3,
            "dexterity": 8,
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
        return -1
    
    @property
    def job_name(self) -> str:
        return "Archer"

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
