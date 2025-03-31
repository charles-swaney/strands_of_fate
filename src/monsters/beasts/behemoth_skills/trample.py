from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
import random


class Trample(Skill):
    """
    A slightly inaccurate but powerful skill that costs both hp and mp, dealing moderate damage
    to all enemies. Cannot critically strike, and does physical damage of type 'misc'. Has a
    0.90 modifier on hit chance.

    Monsters:
        - Behemoth
    """
    def __init__(self):
        super().__init__(
            name="Trample",
            cost_type="mp",
            base_cost=8,
            cost_scaling=2.0,
            cooldown=3,
            magnitude=0.75,
            element=None,
            skill_type="damage"
        )
        self.target_type="all"

    def execute(self,
                caster: Union[Adventurer, Monster],
                targets: List[Adventurer],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_hp(-cost)
        caster.update_mp(-cost)

        for target in targets:
            damage = compute_damage_physical(
                attacker=caster,
                defender=target,
                attack_type="ability",
                weapon_dmg_type="misc",
                multipliers=[self.magnitude] + list(other_multipliers)
            )
            # Skill is slightly inaccurate
            hit_chance = compute_hit_chance(caster, target, 0.90)
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
        if caster.hp < cost:
            return False
        return True
