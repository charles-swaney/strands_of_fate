#!/bin/bash

JOB_NAME=$1
SUBDIR=$2

CLASS_NAME=$(echo "$JOB_NAME" | sed -E 's/(^|_)([a-z])/\U\2/g')
LOWERCASE_JOB_NAME=$(echo "$JOB_NAME" | tr '[:upper:]' '[:lower:]')

OUTPUT_FILE="src/jobs/$SUBDIR/${LOWERCASE_JOB_NAME}.py"

cat <<EOF > "$OUTPUT_FILE"
from jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus

if TYPE_CHECKING:
    from src.adventurers.adventurer import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class $CLASS_NAME(Job):
    """
    Describe the $CLASS_NAME class.

    Key Traits:
    -
    -
    -

    Weapons:
    -

    Armor:
    -

    Growths:
        "hp": TODO,
        "mp": TODO,
        "strength": TODO,
        "toughness": TODO,
        "dexterity": TODO,
        "agility": TODO,
        "intellect": TODO,
        "wisdom": TODO,
        "speed": TODO,
        "tenacity": TODO,
        "charisma": TODO,
        "luck": TODO
    """

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: TODO
        return {
            "hp": TODO,
            "mp": TODO,
            "strength": TODO,
            "toughness": TODO,
            "dexterity": TODO,
            "agility": TODO,
            "intellect": TODO,
            "wisdom": TODO,
            "speed": TODO,
            "tenacity": TODO,
            "charisma": TODO,
            "luck": TODO
        }

    @property
    def class_aptitude(self) -> int:
        return TODO

    @property
    def job_name(self) -> str:
        return "$JOB_NAME"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": [],
            "armor": ["heavy_armor", "light_armor", "robe"],
            "gauntlet": ["heavy_armor", "light_armor", "robe"],
            "greaves": ["heavy_armor", "light_armor", "robe"],
            "helmet": ["heavy_armor", "light_armor", "robe"],
            "accessory": ["ring", "necklace"],
            "shield": ["shield"]
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "strength": 100
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({})

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
            if adventurer.deterministic:
                bonus_mult = 0
            else:
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
EOF
