from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from src.utils.stat_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Hemomancer(Job):
    """
    An advanced class that casts spells using hp instead of mp. Wields the
    formidable power of blood magic to heal themselves while dealing damage.

    Key Traits:
    - Incredible hp and intellect growth.
    - Very poor other growths for an advanced class, and -1 aptitude.
    - Abilities afford them massive tankiness and damage, provided
        they have the hp to sustain their casting.
    - Poor stat growth is offset by very strong class abilities.

    Weapons:
    - Rods, Daggers

    Armor:
    - Robes
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 44
        return {
            "hp": 10,
            "mp": 1,
            "strength": 2,
            "toughness": 5,
            "dexterity": 4,
            "agility": 4,
            "intellect": 9,
            "wisdom": 5,
            "speed": 5,
            "tenacity": 4,
            "charisma": 1,
            "luck": 6
        }

    @property
    def class_aptitude(self) -> int:
        return -1

    @property
    def job_name(self) -> str:
        return "Hemomancer"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["rod", "dagger"],
            "armor": ["robe"],
            "gauntlet": ["robe"],
            "greaves": ["robe"],
            "helmet": ["robe"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "hp": 200,
            "intellect": 100
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({})

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
