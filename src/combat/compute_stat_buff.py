from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from core.stats.attributes import Attributes
from math import prod

BASE_BUFF = 5
CHARISMA_MULT = 0.25
LUCK_MULT = 0.05
BASE_TARGET_STAT_MULT = 0.05
CHARISMA_TARGET_STAT_MULT = 0.0004

def compute_stat_buff(caster: Union[Adventurer, Monster],
                      target: Union[Adventurer, Monster],
                      stats_affected = List[str],
                      multipliers: List[float] = []) -> Attributes:
    """
    Computes the magnitude of the stat buff. A stat buff is any buffing spell that increases one
    or more of the target's stats by some amount. 

    Args:
        caster: the unit casting the stat buff.
        target: the target receiving the stat buff.
        stats: the list of stats to apply the buff to.
        multipliers: multipliers to attach to the heal, e.g. from healing boosts, heal received
            debuffs, and other such ad hoc factors.
    Returns:
        Attributes: an Attributes class containing all the attributes and the buff amounts,
            which can be easily applied to target.

    Note: buff amount is deterministic.
    """

    if multipliers is None:
        multipliers = []
    
    stat_dct = {}
    
    for stat in stats_affected:
        stat_increase = compute_increase_amount(caster=caster,
                                                target=target,
                                                stat=stat,
                                                multipliers=multipliers)
        stat_dct[stat] = stat_increase
    
    stat_attributes = Attributes(stat_dct)
    return stat_attributes

def compute_increase_amount(caster: Union[Adventurer, Monster],
                      target: Union[Adventurer, Monster],
                      stat = str,
                      multipliers: List[float] = []) -> float:
    """
    Returns the amount a given stat increases when caster casts buff on target.
    """
    charisma = caster.total_stats.get_stat("charisma")
    luck = caster.total_stats.get_stat("luck")
    buffed_stat = target.total_stats.get_stat(stat)

    base_buff = BASE_BUFF + (CHARISMA_MULT * charisma) + (LUCK_MULT * luck)
    stat_based_buff = buffed_stat * (BASE_TARGET_STAT_MULT + CHARISMA_TARGET_STAT_MULT * charisma)

    final = base_buff + stat_based_buff
    final_buff = final * prod(multipliers) if multipliers else final
    
    return final_buff
