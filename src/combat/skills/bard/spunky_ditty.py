from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from combat.compute_stat_buff import compute_stat_buff

class SpunkyDitty(Skill):
    def __init__(self):
        super().__init__(
            name="SpunkyDitty",
            cost_type="mp",
            base_cost=12,
            cost_scaling=3.0,
            cooldown=6,
            magnitude=1.0,
            element=None,
            skill_type="buff"
        )
        self.target_type="all"
        self.stats_affected = ["strength", "intellect", "agility", "luck"]

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        if len(targets) > 4:
            raise ValueError(f"Cannot cast on {len(targets)} targets.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            buffs = compute_stat_buff(
                caster=caster,
                target=target,
                stats_affected=self.stats_affected
            )
            target.stat_buffs.update(buffs)

        self.remaining_cooldown = self._cooldown
