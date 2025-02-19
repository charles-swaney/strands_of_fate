from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class SpellBlade(Job):
    """
    A melee hybrid class that is able to attack competently with their weapons
    and spells alike.

    Key Traits:
    - Very balanced stat growths, but weak defensive stats.
    - Other growths are moderate across 
    - Abilities allow them to deal damage in both melee and magical combat.

    Weapons:
    - Swords, Rods

    Armor:
    - Light armor, Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 51
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
            "charisma": 5,
            "luck": 6
        }

    @property
    def class_aptitude(self) -> int:
        return -0.5
    
    @property
    def job_name(self) -> str:
        return "SpellBlade"
    
    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["rod", "sword"],
            "armor": ["robe", "light_armor"],
            "gauntlet": ["robe", "light_armor"],
            "greaves": ["robe", "light_armor"],
            "helmet": ["robe", "light_armor"],
            "accessory": ["ring", "necklace"],
            "shield": ["shield"]
        }
    
    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "strength": 60,
            "intellect": 60
        })
    
    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "BlackMage": 5,
            "Warrior": 5
        })

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
            adventurer.base_stats.add_to_stat(
                stat,
                growth_rate + (bonus_mult * stat_bonus)
            )
