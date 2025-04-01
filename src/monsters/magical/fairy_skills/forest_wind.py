from typing import List
from actions.skill import Skill
from monsters.monster import Monster
from combat.compute_heal import compute_heal


class ForestWind(Skill):
    """
    Moderately heals a single ally.

    Monsters:
        - Fairy
    """
    def __init__(self):
        super().__init__(
            name="Forest Wind",
            cost_type="mp",
            base_cost=8,
            cost_scaling=1.65,
            cooldown=2,
            magnitude=1.0,
            element=None,
            skill_type="heal"
        )
        self.target_type = "single"

    def execute(self,
                caster: Monster,
                targets: List[Monster],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        if len(targets) > 1:
            raise ValueError(f"Cannot cast on {len(targets)} targets.")

        cost = self.cost(caster)

        caster.update_mp(-cost)

        heal_value = 8 + compute_heal(caster=caster, multipliers=list(other_multipliers))

        for target in targets:
            target.update_hp(heal_value)

        self.remaining_cooldown = self._cooldown
