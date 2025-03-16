from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer


class ElementalHarmony(Skill):
    def __init__(self):
        """
        Raises strength proportional to the unit's intellect, and raises intellect proportional
        to the unit's strength, for three turns.
        """
        super().__init__(
            name="Elemental Harmony",
            cost_type="mp",
            base_cost=10,
            cost_scaling=1.50,
            cooldown=5,
            magnitude=1.00,
            element="neutral",
            skill_type="buff"
        )
        self.target_type="self"

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)
        caster.update_hp(-cost)

        for target in targets:

            strength_bonus = target.intellect * 0.25
            intellect_bonus = target.strength * 0.25

            target.stat_buffs.update(
                {
                    "strength": strength_bonus,
                    "intellect": intellect_bonus
                }
            )

        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Adventurer):
        cost = self.cost(caster)
        if caster.mp < cost or self.remaining_cooldown > 0:
            return False
        if caster.hp < cost or self.remaining_cooldown > 0:
            return False
        return True
