from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Knight(Job):
    """
    A well-rounded melee class with high tenacity, strong defense, and access
    to basic healing abilities.

    Key Traits:
    - Good growth in toughness and tenacity.
    - Respectable wisdom growth allows for non-trivial healing.
    - Low speed growth and worse offensive capabilities than Warriors.
    - Abilities range from minor support to damage-dealing.

    Weapons:
    - Swords, Hammers

    Armor:
    - Heavy armor, Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 49
        return {
            "hp": 7,
            "mp": 3,
            "strength": 6,
            "toughness": 8,
            "dexterity": 5,
            "agility": 4,
            "intellect": 3,
            "wisdom": 5,
            "speed": 3,
            "tenacity": 8,
            "charisma": 5,
            "luck": 2
        }
    
    @property
    def class_aptitude(self) -> int:
        return 0.5
    
    @property
    def job_name(self) -> str:
        return "Knight"
    
    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["sword", "hammer"],
            "armor": ["heavy_armor", "robe"],
            "gauntlet": ["heavy_armor", "robe"],
            "greaves": ["heavy_armor", "robe"],
            "helmet": ["heavy_armor", "robe"],
            "accessory": ["ring", "necklace"],
            "shield": ["shield"]
        }
    
    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "strength": 75,
            "wisdom": 44,
            "tenacity": 55
        })
    
    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Warrior": 5,
            "WhiteMage": 5
        })

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
            adventurer.base_stats.add_to_stat(
                stat,
                growth_rate + (bonus_mult * stat_bonus)
            )
