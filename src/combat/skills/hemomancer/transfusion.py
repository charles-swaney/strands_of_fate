from actions.spell import Spell
from combat.damage_calculator import compute_damage_magical
from combat.debuff_hit_chance import compute_debuff_chance
from combat.hit_chance import compute_hit_chance
import random


class Transfusion(Spell):
    def __init__(self):
        super().__init__(
            name="Fire",
            cost_type="mp",
            base_cost=0,
            cost_scaling=2.0,
            cooldown = 2,
            magnitude=0.75,
            element = "fire",  # Temporarily, until I implement a neutral elemental damage type.
            spell_type="damage"
        )
        self.target_type = "single"
        self.drain_factor = 0.40

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

        # Apply spell effect
        for target in targets:
            damage = compute_damage_magical(caster, target, attack_element=self.element, magnitude=self.magnitude, *other_multipliers)
            hit_chance = compute_hit_chance(caster, target, 1.05)
            hit_roll = random.random()
            if hit_roll < hit_chance:
                target.update_hp(-damage)
                caster.update_hp(self.drain_factor * damage)

        self.remaining_cooldown = self._cooldown
