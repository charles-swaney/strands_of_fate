from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer


class SpellBlade(Job):
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 48
        return {
            "hp": 6,
            "mp": 5,
            "strength": 6,
            "toughness": 4,
            "dexterity": 6,
            "agility": 6,
            "intellect": 6,
            "wisdom": 4,
            "speed": 5,
            "tenacity": 3,
            "charisma": 4,
            "luck": 4
        }

    @property
    def class_aptitude(self) -> int:
        return -0.5
    
    @property
    def job_name(self) -> str:
        return "SpellBlade"

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
