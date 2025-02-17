from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer


class Hemomancer(Job):
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 41
        return {
            "hp": 10,
            "mp": 0,
            "strength": 2,
            "toughness": 5,
            "dexterity": 4,
            "agility": 4,
            "intellect": 9,
            "wisdom": 5,
            "speed": 5,
            "tenacity": 3,
            "charisma": 1,
            "luck": 3
        }

    @property
    def class_aptitude(self) -> int:
        return -1
    
    @property
    def job_name(self) -> str:
        return "Hemomancer"

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
            adventurer.base_stats[stat] += growth_rate + (bonus_mult * stat_bonus)
