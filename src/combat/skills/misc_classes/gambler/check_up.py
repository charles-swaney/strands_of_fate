from typing import List
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from combat.compute_stat_buff import compute_stat_buff
import random
import math


class CheckUp(Skill):
    def __init__(self):
        super().__init__(
            name="Check Up",
            cost_type="mp",
            base_cost=5,
            cost_scaling=1.5,
            cooldown=3,
            magnitude=0.75,
            element=None,
            skill_type="buff"
        )
        self.target_type="single"
        self.all_attributes = ["strength", "toughness", "dexterity", "agility",
                               "intellect","wisdom", "speed", "tenacity", "charisma", "luck"]

    def execute(self,
                caster: Adventurer,
                targets: List[Adventurer]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            stat_affected = random.choice(self.all_attributes)
            stats_affected = [stat_affected]

            buffs = compute_stat_buff(
                caster=caster,
                target=target,
                stats_affected=stats_affected,
                multipliers=[self.magnitude]
            )
            target.stat_buffs.update(buffs)
        
        for _ in range(3):
            suit = random.choice(['spade', 'heart'])
            value = random.randint(0, 9)
            caster.job.add_card(suit=suit, value=value)

        self.remaining_cooldown = self._cooldown
