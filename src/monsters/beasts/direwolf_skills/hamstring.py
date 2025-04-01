from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
from combat.debuff_hit_chance import compute_debuff_chance
import random


class Hamstring(Skill):
    """
    A precise physical strike that deals moderate damage to a target with a chance of lowering
    the target's agility. Cannot critically strike.

    Monsters:
        - Dire Wolf
    """
    def __init__(self):
        super().__init__(
            name="Hamstring",
            cost_type="mp",
            base_cost=5,
            cost_scaling=1.25,
            cooldown=3,
            magnitude=0.80,
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
                attack_type="ability",
                weapon_dmg_type="slash",
                multipliers=[self.magnitude] + list(other_multipliers)
            )

            hit_chance = compute_hit_chance(caster, target)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
                debuff_roll = random.random()
                debuff_chance = compute_debuff_chance(
                    attacker=caster,
                    defender=target,
                    type="physical"
                )

                if debuff_roll < debuff_chance:
                    agi_value = target.agility / 3
                    target.base_stats.update(Attributes({"agility": -agi_value}))

        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Monster):
        cost = self.cost(caster)
        if self.remaining_cooldown > 0:
            return False
        if caster.mp < cost:
            return False
        return True
