from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from math import prod
import random
BASE_HIT_CHANCE = 0.95


def compute_hit_chance(
        attacker: Union[Monster, Adventurer],
        defender: Union[Monster, Adventurer],
        *other_multipliers: List[float]
        ) -> float:
    """
    A formula for computing the hit chance between attacker and defender.

    Args:
        attacker: the Monster or Adventurer doing the attack
        defender: the Monster or Adventurer being attacked
        other_multipliers: a list of other multipliers, e.g. a unit having exceptionally high
            dodge rate, magic having higher natural hit rate, etc.

    Returns:
        float: the probability that the attack lands successfully.

    Notes:
        - The formula is primarily driven by the interplay between attacker dexterity and
        defender agility, as well as both units' luck, with the defender's having a larger
        effect (it seems more luck is involved in dodging things than in hitting things.)
        - When dex and agi are equal, we recover 1.02 * BASE_HIT_RATE (modulo the luck ratio)
    """
    attacker_dex = attacker.get_total_stat("dexterity")
    attacker_luck = attacker.get_total_stat("luck")

    defender_agi = defender.get_total_stat("agility")
    defender_luck = defender.get_total_stat("luck")

    main_contribution = ((BASE_HIT_CHANCE * 2) *
                         1.02 * attacker_dex / (attacker_dex + defender_agi))
    luck_ratio = 1 + (0.10 * attacker_luck / (attacker_luck + 1.20 * defender_luck))

    base_chance = main_contribution * luck_ratio

    final_chance = base_chance * prod(other_multipliers) if other_multipliers else base_chance

    final_chance += random.uniform(-0.05, 0.05)

    return max(0.10, min(0.995, final_chance))
