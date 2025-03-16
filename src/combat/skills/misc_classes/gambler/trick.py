from typing import List, Union
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
import random
import math


class TrickUpTheSleeve(Skill):
    def __init__(self):
        super().__init__(
            name="Trick up the Sleeve",
            cost_type="mp",
            base_cost=6,
            cost_scaling=1.5,
            cooldown=2,
            magnitude=0.9,
            element=None,
            skill_type="damage"
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

        for target in targets:
            damage = compute_damage_physical(
                attacker=caster,
                defender=target,
                attack_type="ability",
                weapon_dmg_type="misc",
                multipliers=[self.magnitude] + list(other_multipliers)
            )

            hit_chance = compute_hit_chance(caster, target)
            hit_roll = random.random()

            if hit_roll < hit_chance:
                caster.job.add_card(suit='spade', value=math.floor(damage))
                target.update_hp(-damage)
            suit = random.choice(['spade', 'heart'])
            value = random.randint(0, 9)
            caster.job.add_card(suit=suit, value=value)

        self.remaining_cooldown = self._cooldown
