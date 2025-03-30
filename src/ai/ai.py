from abc import ABC, abstractmethod
from typing import Union
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from actions.action import Action


class AIBehavior(ABC):
    def __init__(self, owner: Union[Adventurer, Monster]):
        self.owner = owner

    @abstractmethod
    def do_action(self, unit: Union[Adventurer, Monster], battle: Battle):
        """
        Executes an action.
        """
        pass
