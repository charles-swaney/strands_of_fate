from typing import Union, Optional
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from actions.action import Action


class Ability(Action):
    """A class defining magic spells."""
    def __init__(self,
                 name: str,
                 cost: int,
                 spell_type: str,
                 magnitude: float,
                 cooldown: int,
                 cost_type: str = 'mp',
                 element: Optional[str] = None,
                 status_effect: Optional[str] = None):
        super().__init__(name, cost_type, cost, "single", cooldown)
        self.spell_type = spell_type
        self.magnitude = magnitude
        self.element = element
        self.status_effect = status_effect
    
