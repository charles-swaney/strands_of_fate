from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer


class Fighter(Job):
    """
    A damage-oriented yet moderately well-rounded melee class.

    Key Traits:
    - Strong strength growth.
    - Other growths are moderate across the board.
    - Abilities exclusively focused on dealing damage in a wide
        variety of ways

    Weapons:
    - Swords, Axes

    Armor:
    - Light armor
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 47
        return {
            "hp": 7,
            "mp": 2,
            "strength": 9,
            "toughness": 5,
            "dexterity": 5,
            "agility": 4,
            "intellect": 2,
            "wisdom": 3,
            "speed": 4,
            "tenacity": 5,
            "charisma": 4,
            "luck": 6
        }

    @property
    def class_aptitude(self) -> int:
        return 0.5
    
    @property
    def job_name(self) -> str:
        return "Fighter"

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
