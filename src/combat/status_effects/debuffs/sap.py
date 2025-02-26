from status_effects.status_effect import StatusEffect, StatusType
from core.stats.attributes import Attributes
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from typing import Union
from math import prod


class Sap(StatusEffect):
    """Decreases the target's toughness."""
    def __init__(self,
                 name="sap",
                 duration: int = 3,
                 magnitude: int = 1.00,
                 stacks: int = 1,
                 max_stacks: int = 2
    ):
        super().__init__(
            name=name,
            status_type=StatusType.DEBUFF,
            duration=duration,
            magnitude=magnitude,
            stacks=stacks,
            max_stacks=max_stacks,
        )

    def calculate_strength(self,
                           caster: Union[Adventurer, Monster],
                           target: Union[Adventurer, Monster],
                           *scaling_factors):

        # Incomplete, needs to account for the target's resistance. This would work for a buff.
        base_strength = self.base_strength(caster)
        sap_strength = base_strength + 0.10 * caster.get_total_stat("toughness")
        scaling_mult = prod(scaling_factors) if scaling_factors else 1.0
        return sap_strength * scaling_mult
    
    def stat_mods(self) -> Attributes:
        total_strength = self.calculate_strength
        return Attributes({"toughness": -total_strength})