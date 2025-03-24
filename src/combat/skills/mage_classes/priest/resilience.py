from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from combat.status_effects.status_effect import StatusEffect


class Resilience(Skill):
    def __init__(self):
        """
        Increases the entire party's resistance to debuffs based on the caster's wisdom and
        charisma.
        """
        super().__init__(
            name="TODO",
            cost_type="mp",
            base_cost=8,
            cost_scaling=1.5,
            cooldown=5,
            magnitude=None,
            element="TODO",
            skill_type="damage"
        )
        self.target_type="single"

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer],
                *other_multipliers):

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            target.status_effects.append(1) # TODO

        self.remaining_cooldown = self._cooldown