from typing import Union, Optional, List, TYPE_CHECKING
from actions.action import Action
from combat.damage_calculator import compute_damage_magical
from combat.debuff_hit_chance import compute_debuff_chance
from combat.hit_chance import compute_hit_chance
from combat.status_effects.status_effect import StatusEffect
import random

if TYPE_CHECKING:
    from adventurers.adventurer import Adventurer
    from monsters.monster import Monster


class Skill(Action):
    """A class defining skills."""
    def __init__(self,
                 name: str,
                 base_cost: int,
                 cost_scaling: float,
                 skill_type: str,
                 magnitude: float,
                 cooldown: int,
                 cost_type: str = 'mp',
                 element: Optional[str] = None,
                 status_effect: Optional[StatusEffect] = None):
        """
        Args:
            name (str): the name of the skill
            base_cost (int): the mp cost of the skill at level 1
            cost_scaling (float): the additional mp cost per level^0.6 gained
            skill_type (str): 'damage', 'heal', 'buff', 'debuff'
            magnitude: the multiplier that roughly measures how powerful the skill is
            cooldown: the number of turns before the skill can be cast again
            cost_type: whether the skill costs hp or mp to cast
            element: the element damage that the skill deals
            status_effect: the status effect conferred by the skill.
        """
        super().__init__(name, cost_type, base_cost, cost_scaling, "single", cooldown)
        self.skill_type = skill_type
        self.magnitude = magnitude
        self.element = element
        self.status_effect = status_effect
        self.remaining_cooldown = 0

    def execute(self,
                caster: Union["Adventurer", "Monster"],
                targets: Union["Adventurer", "Monster", List["Adventurer"], List["Monster"]],
                *other_multipliers) -> None:
        
        if not isinstance(targets, (list, tuple)):
            targets = [targets]

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        if self.target_type == "single":
            if len(targets) > 1:
                raise ValueError(f"Cannot cast {self.name} on {len(targets)} targets.")

        cost = self.cost(caster)

        if self.cost_type == 'mp':
            if caster.mp < cost:
                raise ValueError("Not enough mp.")
            caster.update_mp(-cost)
        elif self.cost_type == 'hp':
            if caster.hp < cost:
                raise ValueError("Not enough hp.")
            caster.update_hp(-cost)

        # Apply skill effect
        if self.skill_type == 'damage':
            for target in targets:
                damage = compute_damage_magical(caster, target, attack_element=self.element, magnitude=self.magnitude, *other_multipliers)
                hit_chance = compute_hit_chance(caster, target, 1.05)
                hit_roll = random.random()
                if hit_roll < hit_chance:
                    target.update_hp(-damage)

        elif self.skill_type == 'heal':
            raise NotImplementedError
        
        elif self.skill_type == 'debuff':
            if self.status_effect:
                for target in targets:
                    success_chance = compute_debuff_chance(caster, target)
                    roll = random.random()
                    if roll < success_chance:
                        self.status_effect.apply_to(target)

        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Union["Adventurer", "Monster"]):
        cost = self.cost(caster)
        if self.cost_type == "mp":
            return self.remaining_cooldown == 0 and cost <= caster.mp
        elif self.cost_type == "hp":
            return self.remaining_cooldown == 0 and cost <= caster.hp
        

    def tick_cooldown(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1
    
    def cost(self, caster: Union["Adventurer", "Monster"]) -> float:
        """Return the cost of the skill."""
        return self.base_cost + self.cost_scaling * (caster.level ** 0.6)
