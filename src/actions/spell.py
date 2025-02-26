from typing import Union, Optional, List
from actions.action import Action
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.damage_calculator import compute_damage_magical
from combat.debuff_hit_chance import compute_debuff_chance
from combat.status_effects.status_effect import StatusEffect
import random


class Spell(Action):
    """A class defining magic spells."""
    def __init__(self,
                 name: str,
                 cost: int,
                 spell_type: str,
                 magnitude: float,
                 cooldown: int,
                 cost_type: str = 'mp',
                 element: Optional[str] = None,
                 status_effect: Optional[StatusEffect] = None):
        """
        Args:
            name (str): the name of the spell
            cost (int): the mp cost of the spell
            spell_type (str): 'damage', 'heal', 'buff', 'debuff'
            magnitude: the multiplier that roughly measures how powerful the spell is
            cooldown: the number of turns before the spell can be cast again
            cost_type: whether the spell costs hp or mp to cast
            element: the element damage that the spell deals
            status_effect: the status  
        """
        super().__init__(name, cost_type, cost, "single", cooldown)
        self.spell_type = spell_type
        self.magnitude = magnitude
        self.element = element
        self.status_effect = status_effect
        self.remaining_cooldown = 0

    def cast(self,
             caster: Union[Adventurer, Monster],
             targets: List[Union[Adventurer, Monster]]) -> None:

        if not self.can_be_cast():
            raise ValueError(f"Cannot cast {self.name}.")

        if self.cost_type == 'mp':
            if caster.mp < self.cost:
                raise ValueError("Not enough mp.")
            caster.update_mp(-self.cost)
        else:
            if caster.hp < self.cost:
                raise ValueError("Not enough hp.")
            caster.update_hp(-self.cost)

        # Apply spell effect
        if self.spell_type == 'damage':
            for target in targets:
                damage = compute_damage_magical(caster, target)
                target.update_hp(-damage)

        elif self.spell_type == 'heal':
            raise NotImplementedError
        
        elif self.spell_type == 'debuff':
            if self.status_effect:
                for target in targets:
                    success_chance = compute_debuff_chance(caster, target)
                    roll = random.random()
                    if roll < success_chance:
                        self.status_effect.apply_to(target)

        self.remaining_cooldown = self._cooldown

    def can_be_cast(self):
        return self.remaining_cooldown == 0
        

    def tick_cooldown(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1
