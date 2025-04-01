from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.damage_calculator import compute_damage_magical
from combat.hit_chance import compute_hit_chance
import random


class StarStream(Skill):
    def __init__(self):
        """
        Deals moderate holy magical damage.

        Monsters:
            - Behemoth
        """
        super().__init__(
            name="Star Stream",
            cost_type="mp",
            base_cost=10,
            cost_scaling=2.0,
            cooldown=3,
            magnitude=0.75,
            element="holy",
            skill_type="damage"
        )
        self.target_type = "single"

    def execute(self,
                caster: Union[Adventurer, Monster],
                targets: List[Adventurer],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            damage = compute_damage_magical(
                attacker=caster,
                defender=target,
                attack_element=self.element,
                magnitude=self.magnitude,
                multipliers=list(other_multipliers)
            )
            hit_chance = compute_hit_chance(caster, target)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)

        self.remaining_cooldown = self._cooldown
