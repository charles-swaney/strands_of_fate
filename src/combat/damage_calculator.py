from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.crit_chance import compute_critical_chance
from math import prod
import random
MAX_DAMAGE = 1999
CRIT_DMG_MULTIPLIER = 1.5


def compute_damage_physical(
    attacker: Union[Monster, Adventurer],
    defender: Union[Monster, Adventurer],
    attack_type: str,
    weapon_dmg_type: str,
    *other_multipliers: List[float]
        ) -> float:
    """
    Compute the damage dealt when attacker hits defender with a physical attack. 
    Note: *other_multipliers does NOT need to include weapon resistances of the defender, ever.
    But, it should include other factors, such as buffs and debuffs, etc.

    Args:
        attacker: the unit attacking.
        defender: the unit defending.
        attack_type: whether the physical damage is from a standard attack, "standard", or a 
            physical-damage ability, "ability". Only the former can crit.
        weapon_type: the weapon type, for purposes of incorporating monster damage resistances.
        other_multipliers: weapon resistances, buffs, etc.
    
    Returns:
        float: the damage dealt.

    Note: casting a physical ability with a certain weapon equipped will STILL apply the weapon
        type bonus, even if technically the ability does not involve literally "swinging" or
        using the weapon. However, it a physical ability will NEVER crit. 
    """
    weapon_bonus = 1.0

    if isinstance(defender, Monster):
        weapon_bonus = defender.get_weapon_res(weapon_type=weapon_dmg_type)

    watk = attacker.watk
    wdef = defender.wdef

    main_dmg = 0.85 * (watk / 1.75 - wdef / 3.75) * weapon_bonus

    final_dmg = main_dmg * prod(other_multipliers) if other_multipliers else main_dmg

    final_dmg *= random.uniform(0.95, 1.05)

    if attack_type == "standard":
        crit_chance = compute_critical_chance(attacker=attacker, defender=defender)
        if random.random() < crit_chance:
            final_dmg *= CRIT_DMG_MULTIPLIER

    return max(1, min(MAX_DAMAGE, final_dmg))


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
        attack_element: the elemental damage type of the spell being cast.
        other_multipliers: weapon resistances, buffs, etc.
    
    Returns:    
        float: the damage dealt.
    """
    elemental_bonus = 1.0

    if isinstance(defender, Monster):
        elemental_bonus = defender.get_element_res(element=attack_element)

    matk = attacker.matk
    mdef = defender.mdef

    main_dmg = 1.15 * (matk / 2 - mdef / 4) * elemental_bonus

    final_dmg = main_dmg * prod(other_multipliers) if other_multipliers else main_dmg

    final_dmg *= random.uniform(0.95, 1.05)

    return max(1, min(MAX_DAMAGE, final_dmg))
