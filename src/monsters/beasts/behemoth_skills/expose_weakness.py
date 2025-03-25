from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
from combat.debuff_hit_chance import compute_debuff_chance
import random


class ExposeWeakness(Skill):
    def __init__(self):
        """
        Deals a small amount of damage, with a high chance of lowering the target's toughness
        and tenacity.

        Monsters:
            - Behemoth
        """
        super().__init__(
            name="Expose Weakness",
            cost_type="mp",
            base_cost=8,
            cost_scaling=2.0,
            cooldown=3,
            magnitude=0.50,
            element=None,
            skill_type="damage"
        )
        self.target_type="single"

    def execute(self,
                caster: Monster,
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
                weapon_dmg_type=caster.weapon_type,
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
                    tgh_value = target.toughness * 0.40
                    ten_value = target.tenacity * 0.40
                    target.base_stats.update(Attributes({"toughness": -tgh_value,
                                                          "tenacity": -ten_value}))
        self.remaining_cooldown = self._cooldown

