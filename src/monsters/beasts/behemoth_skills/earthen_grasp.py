from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from combat.damage_calculator import compute_magical_raw
from combat.hit_chance import compute_hit_chance
from combat.debuff_hit_chance import compute_debuff_chance
import random


class EarthenGrasp(Skill):
    def __init__(self):
        """
        Deals moderate earth damage, while lowering dexterity and agility.

        Monsters:
            - Behemoth
        """
        super().__init__(
            name="Earthen Grasp",
            cost_type="mp",
            base_cost=10,
            cost_scaling=2.0,
            cooldown=3,
            magnitude=0.75,
            element="earth",
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
            attack_value = caster.watk
            damage = compute_magical_raw(
                attack_value=attack_value,
                defender=target,
                attack_element=self.element,
                magnitude=self.magnitude,
                multipliers=list(other_multipliers)
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
                    dex_value = target.dexterity / 3
                    agi_value = target.agility / 3
                    target.base_stats.update(Attributes({"dexterity": -dex_value,
                                                         "agility": -agi_value}))
        self.remaining_cooldown = self._cooldown
