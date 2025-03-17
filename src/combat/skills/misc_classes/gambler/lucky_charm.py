from typing import List, Union
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from combat.compute_heal import compute_heal_raw
import random
import math


class LuckyCharm(Skill):
    def __init__(self):
        super().__init__(
            name="Lucky Charm",
            cost_type="mp",
            base_cost=8,
            cost_scaling=2.0,
            cooldown=3,
            magnitude=0.30,
            element=None,
            skill_type="heal"
        )
        self.target_type="single"
    
    def execute(self,
                caster: Union[Adventurer, Monster],
                targets: Union[Adventurer, Monster],
                *other_multipliers) -> None:

        if not self.can_be_used(caster=caster):
            raise ValueError(f"Cannot cast {self.name}")

        if not isinstance(caster, Adventurer) or not (caster.job.job_name == "Gambler"):
            raise ValueError(f"Only Gamblers can cast {self.name}")

        cost = self.cost(caster=caster)

        caster.update_mp(-cost)

        multipliers = [self.magnitude] + list(other_multipliers)

        heal_amount = 5 + compute_heal_raw(caster.luck, multipliers=multipliers)
        caster.job.add_card(suit='heart', value=math.floor(heal_amount))
        for target in targets:
            target.update_hp(heal_amount)

        suit = random.choice(['spade', 'heart'])
        value = random.randint(0, 9)
        caster.job.add_card(suit=suit, value=value)

        self.remaining_cooldown = self._cooldown
