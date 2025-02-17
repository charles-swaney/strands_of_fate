from src.jobs.job import Job
from typing import Dict
from src.jobs.job import Adventurer
from src.adventurers.stat_growth import compute_stat_bonus


class Bard(Job):
    @property
    def base_growth_rates(self) -> Dict[str, int]:
        # Total: 45
        return {
            "hp": 5,
            "mp": 5,
            "strength": 3,
            "toughness": 3,
            "dexterity": 5,
            "agility": 5,
            "intellect": 4,
            "willpower": 4,
            "tenacity": 4,
            "charisma": 9,
            "luck": 8
        }
    
    @property
    def class_aptitude(self) -> int:
        return 1

    def apply_level_up(self, adventurer: Adventurer) -> None:
        base_growth_rates = self.base_growth_rates

        for stat, growth_rate in base_growth_rates.items():
            if stat <= 7:
                bonus_mult = 1
            else:
                bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=adventurer.aptitude,
                class_aptitude=self.class_aptitude
                )
            adventurer[stat] += growth_rate + bonus_mult * stat_bonus
