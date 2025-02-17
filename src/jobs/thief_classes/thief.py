from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer


class Thief(Job):
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

    def apply_level_up(self, adventurer: Adventurer) -> None:
        base_growth_rates = self.base_growth_rates

        for stat, growth_rate in base_growth_rates.items():
            if stat <= 3:
                bonus_mult = 0.5
            elif stat >= 4 and stat <= 8:
                bonus_mult = 1
            else:
                bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=adventurer.aptitude,
                class_aptitude=self.class_aptitude)
            
            adventurer.base_stats[stat] += growth_rate + (bonus_mult * stat_bonus)
