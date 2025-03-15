from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
import random
from math import prod

MAX_HEAL = 999
MIN_HEAL = 1


def compute_heal(caster: Union[Adventurer, Monster],
                 multipliers: List[float] = []) -> float:
    """
    Computes the heal value when caster casts a skill with type "heal". 

    Args:
        caster: the unit casting the spell.
        multipliers: multipliers to attach to the heal, e.g. from healing boosts, heal received
            debuffs, and other such ad hoc factors.
    Returns:
        float: the value of the heal.

    Note: only depends on the caster.
    """

    if multipliers is None:
        multipliers = []

    wisdom = caster.wisdom
    charisma = caster.charisma
    luck = caster.luck

    main_heal = 1.05 * (0.30 * wisdom + 0.10 * charisma + 0.03 * luck)

    final_heal = main_heal * prod(multipliers) if multipliers else main_heal

    final_heal *= random.uniform(0.95, 1.05)

    return max(MIN_HEAL, min(MAX_HEAL, final_heal))
