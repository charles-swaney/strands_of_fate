from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING
from src.adventurers.stat_growth import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer


class Bard(Job):
    """
    A class entirely focused on buffing allies, and keeping morale high.

    Key Traits:
    - Very good charisma and luck growths.
    - Other growths are somewhat balanced across the board, with less
        emphasis on melee combat.
    - Has access to the widest range of ally buffing abilities in the game.

    Weapons:
    - Swords, Bows, Poles

    Armor:
    - Light armor, Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 49
        return {
            "hp": 5,
            "mp": 5,
            "strength": 3,
            "toughness": 3,
            "dexterity": 5,
            "agility": 5,
            "intellect": 4,
            "wisdom": 4,
            "speed": 5,
            "tenacity": 3,
            "charisma": 9,
            "luck": 8
        }
    
    @property
    def class_aptitude(self) -> int:
        return 1
    
    @property
    def job_name(self) -> str:
        return "Bard"

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        base_growth_rates = self.growth_rates

        for stat, growth_rate in base_growth_rates.items():
            if growth_rate <= 7:
                bonus_mult = 1
            else:
                bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=adventurer.aptitude,
                class_aptitude=self.class_aptitude
                )
            adventurer.base_stats[stat] += growth_rate + (bonus_mult * stat_bonus)
