from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
import random


class SavageBite(Skill):
    """
    A slightly inaccurate attack that deals more damage the lower the target's hp is
    Can critically strike, but costs both hp and mp.

    Dire Wolves boast a better hp bonus than wolves. Wolves gain 1% damage per 1% hp below
    50%, while Dire Wolves gain a 2% damage bonus per 1% hp below 50%.

    Monsters:
        - Dire Wolf
        - Wolf
    """
    def __init__(self):
        super().__init__(
            name="Savage Bite",
            cost_type="mp",
            base_cost=10,
            cost_scaling=1.5,
            cooldown=3,
            magnitude=1.00,
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
        caster.update_hp(-2 * cost)

        for target in targets:
            hp_ratio = target.hp / target.max_hp
            hp_bonus = 1.0

            if hp_ratio <= 0.50:  # Can implement as match if more units come to learn this skill
                hp_bonus = 1.0 + 2 * (0.50 - hp_ratio) if caster.name == "Dire Wolf" else \
                    1.0 + (0.50 - hp_ratio)

            damage = compute_damage_physical(
                attacker=caster,
                defender=target,
                attack_type="standard",
                weapon_dmg_type="slash",
                multipliers=[self.magnitude] + list(other_multipliers) + [hp_bonus]
            )

            hit_chance = compute_hit_chance(caster, target)
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
        if caster.hp < cost * 2.0:
            return False
        return True
