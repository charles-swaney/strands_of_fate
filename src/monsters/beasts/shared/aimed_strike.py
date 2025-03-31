from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
import random


class AimedStrike(Skill):
    """
    A precise physical strike that deals moderate damage to a target. Can critically strike.
    Does 70% damage, with 133% accuracy.

    Monsters:
        - Wolf
        - Dire Wolf
    """
    def __init__(self):
        super().__init__(
            name="Aimed Strike",
            cost_type="mp",
            base_cost=5,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=0.70,
            element=None,
            skill_type="damage"
        )
        self.target_type="single"

    def execute(self,
                caster: Union[Adventurer, Monster],
                targets: List[Adventurer],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            damage = compute_damage_physical(
                attacker=caster,
                defender=target,
                attack_type="standard",
                weapon_dmg_type="slash",
                multipliers=[self.magnitude] + list(other_multipliers)
            )

            hit_chance = compute_hit_chance(caster, target, 1.33)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Monster):
        cost = self.cost(caster)
        if self.remaining_cooldown > 0:
            return False
        if caster.mp < cost:
            return False
        return True
