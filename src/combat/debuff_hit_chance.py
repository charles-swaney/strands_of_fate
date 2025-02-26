from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from math import prod
import random
BASE_DEBUFF_CHANCE = 0.40


def compute_debuff_chance(
        attacker: Union[Monster, Adventurer],
        defender: Union[Monster, Adventurer],
        *other_multipliers: List[float]
        ) -> float:
    """
    A formula for computing the debuff chance between attacker and defender.

    Args:
        attacker: the Monster or Adventurer applying the debuff
        defender: the Monster or Adventurer being debuffed
        other_multipliers: a list of other multipliers, e.g. bonus effects to debuffs, resilience,
            etc.

    Returns:
        float: the probability that the debuff is successfully applied.

    Notes:
        - The debuff probability is determined by the attacker's intellect/charisma, the defender's
            wisdom/tenacity, and both of their lucks
    """
    attacker_intellect = attacker.get_total_stat("intellect")
    attacker_charisma = attacker.get_total_stat("charisma")
    attacker_luck = attacker.get_total_stat("luck")

    defender_wisdom = defender.get_total_stat("wisdom")
    defender_tenacity = defender.get_total_stat("tenacity")
    defender_luck = defender.get_total_stat("luck")

    attack_weight = 0.3 * attacker_intellect + 0.7 * attacker_charisma
    defense_weight = 0.3 * defender_wisdom + 0.7 * defender_tenacity

    main_contribution = (2 * BASE_DEBUFF_CHANCE *
                            attack_weight / (attack_weight + defense_weight))
    
    luck_ratio = 1 + (0.10 * attacker_luck / (attacker_luck + 1.20 * defender_luck))

    base_chance = main_contribution * luck_ratio

    final_chance = base_chance * prod(other_multipliers) if other_multipliers else base_chance

    return max(0.01, min(0.75, final_chance))