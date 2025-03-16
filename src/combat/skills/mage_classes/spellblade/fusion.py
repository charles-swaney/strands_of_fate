from actions.skill import Skill
from typing import Union, List
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from combat.damage_calculator import compute_magical_raw
from combat.hit_chance import compute_hit_chance
import random


class Fusion(Skill):
    def __init__(self):
        """
        Deals damage to a single target, harnessing both physical and magical energy to strike
        a blow. Deals MAGICAL damage equal to 0.60 * matk + 0.60 * intellect. Specifically,
        instead of calling compute_damage_magical with just matk, it calls it with the above value.

        Damage formula:
            damage = 0.60 * matk + 0.60 * intellect
        """
        super().__init__(
            name="TODO",
            cost_type="mp",
            base_cost=6,
            cost_scaling=1.30,
            cooldown=2,
            magnitude=1.10,
            element="neutral",
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

        attack_value = 0.6 * caster.watk + 0.6 * caster.matk

        for target in targets:
            damage = compute_magical_raw(
                attack_value=attack_value,
                defender=target,
                attack_element="neutral",
                magnitude=self.magnitude,
                multipliers = list(other_multipliers)
            )
            hit_chance = compute_hit_chance(caster, target)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
        self.remaining_cooldown = self._cooldown