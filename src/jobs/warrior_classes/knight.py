from src.jobs.job import Job
from typing import Dict
from src.jobs.job import Adventurer
from src.adventurers.stat_growth import compute_stat_bonus


class Knight(Job):
    @property
    def base_growth_rates(self) -> Dict[str, int]:
        # Total: 46
        return {
            "hp": 7,
            "mp": 3,
            "strength": 6,
            "toughness": 8,
            "dexterity": 5,
            "agility": 4,
            "intellect": 3,
            "willpower": 5,
            "tenacity": 8,
            "charisma": 5,
            "luck": 2
        }
    
    @property
    def class_aptitude(self) -> int:
        return 1

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
                class_aptitude=self.class_aptitude
                )
            adventurer[stat] += growth_rate + bonus_mult * stat_bonus
