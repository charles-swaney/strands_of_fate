from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from math import prod
import random


def compute_damage_physical(
    attacker: Union[Monster, Adventurer],
    defender: Union[Monster, Adventurer],
    *other_multipliers: List[float]
        ) -> float:
    """
    Compute the damage dealt when attacker hits defender with a physical attack. 
    Note: *other_multipliers should ALWAYS include weapon resistance if defender is a Monster.

    Args:
        attacker: the unit attacking.
        defender: the unit defending.
        other_multipliers: weapon resistances, buffs, etc.
    
    Returns:
        float: the damage dealt.
    """

    watk = attacker.watk
    wdef = defender.wdef

    main_dmg = 1.15 * (watk / 2 - wdef / 4)

    final_dmg = main_dmg * prod(other_multipliers) if other_multipliers else main_dmg

    final_dmg *= random.uniform(0.95, 1.05)

    return final_dmg


def compute_damage_magical(
        attacker: Union[Monster, Adventurer],
        defender: Union[Monster, Adventurer],
        attack_element: str,
        *other_multipliers: List[float]
        ) -> float:
    """
    Compute the damage dealt when attacker hits defender with a physical attack. 
    Note: *other_multipliers does NOT need to include elemental resistance: this is ALWAYS
    computed. But, it could include other factors like magic resistance buffs or debuffs, etc.

    Args:
        attacker: the unit attacking.
        defender: the unit defending.
        other_multipliers: weapon resistances, buffs, etc.
    
    Returns:
        float: the damage dealt.
    """
    elemental_bonus = 1.0
    if isinstance(defender, Monster):
        elemental_bonus = defender.get_element_res(attack_element)

    matk = attacker.matk
    mdef = defender.mdef

    main_dmg = 1.15 * (matk / 2 - mdef / 4)

    final_dmg = main_dmg * elemental_bonus

    final_dmg = main_dmg * prod(other_multipliers) if other_multipliers else main_dmg

    final_dmg *= random.uniform(0.95, 1.05)

    return final_dmg
