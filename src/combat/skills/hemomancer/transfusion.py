from actions.skill import Skill
from combat.damage_calculator import compute_damage_magical
from combat.hit_chance import compute_hit_chance
import random


class Transfusion(Skill):
    def __init__(self):
        super().__init__(
            name="Transfusion",
            cost_type="hp",
            base_cost=4,
            cost_scaling=2.0,
            cooldown=2,
            magnitude=0.80,
            element="neutral",
            skill_type="damage"
        )
        self.target_type="single"
        self.drain_factor=0.40

    def execute(self,
                caster,
                targets,
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        cost = self.cost(caster)
        if caster.hp < cost:
            raise ValueError("Not enough hp.")
        caster.update_hp(-cost)

        for target in targets:
            damage = compute_damage_magical(caster, target, attack_element=self.element, magnitude=self.magnitude, *other_multipliers)
            hit_chance = compute_hit_chance(caster, target, 1.05)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
                healing = min(caster.total_stats.get_stat("hp") - caster.hp, self.drain_factor * damage)
                caster.update_hp(healing)
                if caster.hp > caster.total_stats.get_stat("hp"):
                    caster.hp = caster.total_stats.get_stat("hp")

        self.remaining_cooldown = self._cooldown
