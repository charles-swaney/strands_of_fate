from typing import List
from actions.skill import Skill
from monsters.monster import Monster


class IronHide(Skill):
    def __init__(self):
        """
        Raises toughness proportional to the unit's tenacity, and raises tenacity proportional
        to the unit's toughness, for three turns each.
        """
        super().__init__(
            name="Iron Hide",
            cost_type="mp",
            base_cost=12,
            cost_scaling=1.75,
            cooldown=5,
            magnitude=0.75,
            element="neutral",
            skill_type="buff"
        )
        self.target_type="self"

    def execute(self,
                caster: Monster,
                targets: List[Monster]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)
        caster.update_hp(-cost)

        for target in targets:

            tenacity_bonus = target.toughness * 0.25
            toughness_bonus = target.tenacity * 0.25

            target.stat_buffs.update(
                {
                    "toughness": toughness_bonus,
                    "tenacity": tenacity_bonus
                }
            )
        # Need to add some sort of logic that makes this only last for 3 rounds or so   

        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Monster):
        cost = self.cost(caster)
        if caster.mp < cost or self.remaining_cooldown > 0:
            return False
        if caster.hp < cost or self.remaining_cooldown > 0:
            return False
        return True
