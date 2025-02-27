from typing import Union, List, TYPE_CHECKING
import random

from actions.action import Action
from combat.damage_calculator import compute_damage_physical
from combat.hit_chance import compute_hit_chance
from combat.crit_chance import compute_critical_chance

if TYPE_CHECKING:
    from monsters.monster import Monster
    from adventurers.adventurer import Adventurer

CRIT_DAMAGE_MULT = 1.50
BLOCKING_EFFECTS = {
    "Stun",
    "Petrify",
    "Stop"
}


class Attack(Action):
    """A class representing a basic physical attack."""
    def __init__(self,
                 name: str="Attack",
                 cost: int=0,
                 target_type: str="single",
                 cost_type: str="mp",
                 cooldown: int=0):
        super().__init__(name, cost, target_type, cost_type, cooldown)
        self.name = name
        self.cost = cost
        self.target_type = target_type
        self.cost_type = cost_type
        self.remaining_cooldown = 0
    
    def execute(self,
                attacker: Union["Adventurer", "Monster"],
                targets: List[Union["Adventurer", "Monster"]]):

        if not self.can_be_used(attacker):
            raise ValueError(f"Cannot attack right now.")
        
        for target in targets:
            hit_chance = compute_hit_chance(attacker, target)
            hit_roll = random.random()

            if hit_roll < hit_chance:
                damage = compute_damage_physical(attacker,
                                                target,
                                                "standard",
                                                attacker.weapon_type)
                target.update_hp(-damage)
            else:
                pass

    def can_be_used(self, attacker: Union["Adventurer", "Monster"]) -> bool:
        """
        A unit can always attack, unless they have a blocking status effect.
        """
        for status in attacker.status_effects():
            if status.name in BLOCKING_EFFECTS:
                return False
        return True
    
    def tick_cooldown(self) -> None:
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1
