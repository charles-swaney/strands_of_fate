from typing import List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from battles.turn_order import get_turn_order


class Battle:
    def __init__(self,
                 adventurers: List[Adventurer],
                 monsters: List[Monster],
                 verbose: bool = False):
        """
        The general Battle class for handling combat.

        Args:
            adventurers (List[Adventurer]): the adventurers participating in the battle.
            monsters (List[Monster]): the monsters participating in the battle.
            verbose (bool): whether to print statements or not (for 'viewing' battles in CLI)
        """
        self.adventurers = adventurers
        self.monsters = monsters
        self.round_count = 0
        self.turn_order = get_turn_order(self.adventurers, self.monsters)
        self.verbose = verbose

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
        self.remove_dead()
        
        if len(self.turn_order) == 0:
            self.turn_order = get_turn_order(self.adventurers, self.monsters)
            self.round_count += 1
            if self.verbose:
                print(f"Starting round {self.round_count}")
        
        current_unit = self.turn_order.pop(0)
        if self.verbose:
            print(f"Current Unit: {current_unit.name}")

        print(f"Action: {current_unit.do_action(self)}")
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
    
    def run_battle(self) -> str:
        """
        Run the battle until one side is defeated.

        Returns:
            str: whichever side won the battle.
        """
        if self.verbose:
            print("Battle beginning.")
        
        while not self.is_battle_over():
            self.next_turn()
            self.tick_cooldowns()
        if all(monster.hp == 0 for monster in self.monsters):
            outcome = "Adventurers win"
        else:
            outcome = "Monsters win"
    
        if self.verbose:
            print(f"Battle over after {self.round_count} rounds. {outcome}")
            adv_hps = [(adv.name, adv.hp) for adv in self.adventurers]
            monster_hps = [(m.name, m.hp) for m in self.monsters]
            print(f"Outcome: Adventurers: {adv_hps}. Monsters: {monster_hps}.")
        
        return outcome
    
    def remove_dead(self) -> None:
        """
        Remove any dead monsters or adventurers from the turn order.
        """
        for unit in self.turn_order:
            if unit.hp == 0:
                self.turn_order.remove(unit)
