from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from combat.compute_heal import compute_heal

class Heal(Skill):
    def __init__(self):
        super().__init__(
            name="Heal",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=1.0,
            element=None,
            skill_type="heal"
        )
        self.target_type="single"

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        if len(targets) > 1:
            raise ValueError(f"Cannot cast on {len(targets)} targets.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        heal_value = 8 + compute_heal(caster=caster)

        for target in targets:
            target.update_hp(heal_value)

        self.remaining_cooldown = self._cooldown