from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Guardian(Job):
    """
    An extremely tanky and support-oriented melee class. Primarily focuses on
    surviving combat, and buffing and healing allies.

    Key Traits:
    - Incredible toughness and tenacity growth.
    - Very low strength, dexterity, agility growth, for a melee fighter.
    - Above-average charisma and wisdom for supporting teammates.
    - Abilities focused on buffing and protecting allies.

    Weapons:
    - Hammers, Rods, Staves

    Armor:
    - Heavy armor, Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 51
        return {
            "hp": 8,
            "mp": 3,
            "strength": 4,
            "toughness": 11,
            "dexterity": 3,
            "agility": 3,
            "intellect": 3,
            "wisdom": 5,
            "speed": 2,
            "tenacity": 10,
            "charisma": 6,
            "luck": 4
        }
    
    @property
    def class_aptitude(self) -> int:
        return 0
    
    @property
    def job_name(self) -> str:
        return "Guardian"
    
    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["rod", "hammer", "staff"],
            "armor": ["heavy_armor", "robe"],
            "gauntlet": ["heavy_armor", "robe"],
            "greaves": ["heavy_armor", "robe"],
            "helmet": ["heavy_armor", "robe"],
            "accessory": ["ring", "necklace"],
            "shield": ["shield"]
        }
    
    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "hp": 200,
            "toughness": 150,
            "tenacity": 120
        })
    
    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Knight": 15,
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