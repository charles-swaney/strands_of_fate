from typing import List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from battles.turn_order import get_turn_order


class Battle:
    def __init__(self,
                 adventurers: List[Adventurer],
                 monsters: List[Monster]):
        self.adventurers = adventurers
        self.monsters = monsters
        self.round_count = 0
        self.turn_order = get_turn_order(self.adventurers, self.monsters)

    def tick_cooldowns(self) -> None:
        """
        Tick all ability cooldowns for all living units.
        """
        for unit in self.turn_order:
            unit.tick_all_cooldowns()

    def tick_status_effects(self) -> None:
        """
        Tick all status effects (e.g. Poison, Bleed, etc.)
        """
        raise NotImplementedError
    
    def next_turn(self):
        """
        Process a single unit's turn. If it's the start of a new round, reinitialize the turn
        order.
        """
        if self.is_battle_over():
            return
        
        if len(self.turn_order) == 0:
            self.turn_order = get_turn_order(self.adventurers, self.monsters)
            self.round_count += 1
        
        current_unit = self.turn_order.pop(0)

        print(f"Current Unit: {current_unit}")
        return current_unit

    def is_battle_over(self) -> bool:
        """
        Returns True if all units on one side are dead, and False otherwise.
        """
        if all(monster.hp == 0 for monster in self.monsters):
            return True
        elif all(adv.hp == 0 for adv in self.adventurers):
            return True
        return False
