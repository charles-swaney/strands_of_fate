from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from combat.compute_heal import compute_heal
from combat.compute_stat_buff import compute_stat_buff

class EmboldeningChant(Skill):
    def __init__(self):
        super().__init__(
            name="Emboldening Chant",
            cost_type="mp",
            base_cost=6,
            cost_scaling=2.0,
            cooldown=5,
            magnitude=1.25,
            element=None,
            skill_type="heal"
        )
        self.target_type="single"
        self.stats_affected = ["toughness"]

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        if len(targets) > 1:
            raise ValueError(f"Cannot cast on {len(targets)} targets.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        heal_value = compute_heal(caster=caster, multipliers=[self.magnitude])

        for target in targets:
            target.update_hp(heal_value)
            buffs = compute_stat_buff(
                caster=caster,
                target=target,
                stats_affected=self.stats_affected
            )
            target.stat_buffs.update(buffs)

        self.remaining_cooldown = self._cooldown