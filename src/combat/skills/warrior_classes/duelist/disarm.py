from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
import random


class Disarm(Skill):
    def __init__(self):
        """
        Deals moderate damage, with a chance of lowering the target's strength.
        """
        super().__init__(
            name="Disarm",
            cost_type="mp",
            base_cost=6,
            cost_scaling=1.0,
            cooldown=3,
            magnitude=0.75,
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
                weapon_dmg_type=caster.weapon_type,
                multipliers=[self.magnitude] + list(other_multipliers)
            )
            hit_chance = compute_hit_chance(caster, target, 0.90)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
                debuff_roll = random.random()
                debuff_chance = None # TODO need something to compute physical debuff application.
                if debuff_roll < debuff_chance:
                    value = target.strength * 0.40
                    target.total_stats.update(Attributes(
                        {
                            "strength": -value
                        }
                    ))
        self.remaining_cooldown = self._cooldown
