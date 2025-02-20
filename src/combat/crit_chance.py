from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from math import prod
import random
BASE_CRIT_CHANCE = 0.03


def compute_critical_chance(
    attacker: Union[Monster, Adventurer],
    defender: Union[Monster, Adventurer],
    *other_multipliers: List[float]
) -> float:
    attacker_luck = attacker.get_total_stat("luck")
    defender_luck = defender.get_total_stat("luck")

    base_chance = (
        BASE_CRIT_CHANCE
        + (attacker_luck ** 0.70) / 150
        - (defender_luck ** 0.70) / 200
    )

    final_chance = base_chance * prod(other_multipliers) if other_multipliers else base_chance

    final_chance += random.uniform(-0.02, 0.02)

    return max(0.01, min(0.240, final_chance))
