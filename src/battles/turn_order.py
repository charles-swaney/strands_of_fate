from typing import List, Union
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
import random


def get_turn_order(adventurers: List[Adventurer],
                   monsters: List[Monster]) -> List[Union[Adventurer, Monster]]:
    """
    Calculates the turn order given the current list of adventurers and monsters.

    For now, just a simple speed-based implementation: apply a slight perturbation to speed to
    avoid pure determinism, but otherwise just go in descending speed order.

    Note: despite popping from the end of a list being more efficient, we put the fastest unit
    at the front of the list for intuitive simplicity, since the length of the lists involved
    should never exceed 10.
    """
    all_units = adventurers + monsters

    combatants = [(unit, unit.speed * random.uniform(0.95, 1.05)) for unit in all_units]

    combatants.sort(key=lambda x: x[1], reverse=True)

    ordered_combatants = [combatant[0] for combatant in combatants]

    return ordered_combatants

