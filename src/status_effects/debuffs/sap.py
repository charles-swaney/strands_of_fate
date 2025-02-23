from status_effects.status_effect import StatusEffect, StatusType
from core.stats.attributes import Attributes


class Sap(StatusEffect):
    """Decreases the target's toughness."""
    def __init__(self,
                 name="sap",
                 duration: int = 3,
                 magnitude: int = 2,
                 stacks: int = 1,
                 max_stacks: int = 2,
                 scaling: float = 2.0
    ):
        super().__init__(
            name=name,
            status_type=StatusType.DEBUFF,
            duration=duration,
            magnitude=magnitude,
            stacks=stacks,
            max_stacks=max_stacks,
            scaling=scaling
        )
    
    def update_stat_mods(self, magnitude, *other_factors):
        total_magnitude = magnitude

        for factor in other_factors:
            total_magnitude *= factor

        total_magnitude *= self.stacks

        total_magnitude *= self.scaling

        return Attributes({"toughness": -total_magnitude})