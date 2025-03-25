from typing import Union, List
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from math import prod
BASE_DEBUFF_CHANCE = 0.40


def compute_debuff_chance(
        attacker: Union[Monster, Adventurer],
        defender: Union[Monster, Adventurer],
        type: str,
        multipliers: List[float] = []
        ) -> float:
    """
    A formula for computing the debuff chance between attacker and defender.

    Args:
        attacker: the Monster or Adventurer applying the debuff
        defender: the Monster or Adventurer being debuffed
        type: whether the debuff is a magically or physically oriented debuff. This affects
            what stat is used to compute the resistances and debuff application probability.
        other_multipliers: a list of other multipliers, e.g. bonus effects to debuffs, resilience,
            etc.

    Returns:
        float: the probability that the debuff is successfully applied.

    Notes:
        - For magical debuffs, the debuff probability is determined by the attacker's
            charisma/intellect, the defender's tenacity/wisdom, and both of their lucks
        - For physical debuffs, the debuff probability is determined by the attacler's
            dexterity/strength, the defender's toughness/agility, and both of their lucks
    """
    if multipliers is None:
        multipliers = []

    if type == "magical":
        attacker_intellect = attacker.intellect
        attacker_charisma = attacker.charisma
        
        defender_wisdom = defender.wisdom
        defender_tenacity = defender.tenacity

        attack_weight = 0.3 * attacker_intellect + 0.7 * attacker_charisma
        defense_weight = 0.3 * defender_wisdom + 0.7 * defender_tenacity

    elif type == "physical":
        attacker_dexterity = attacker.dexterity
        attacker_strength = attacker.strength

        defender_agility = defender.agility
        defender_toughness = defender.toughness

        attack_weight = 0.3 * attacker_strength + 0.7 * attacker_dexterity
        defense_weight = 0.3 * defender_agility + 0.7 * defender_toughness

    else:
        raise ValueError(f"Invalid debuff type: {type}.")
    
    attacker_luck = attacker.luck
    defender_luck = defender.luck

    main_contribution = (2 * BASE_DEBUFF_CHANCE *
                            attack_weight / (attack_weight + defense_weight))
    
    luck_ratio = 1 + (0.10 * attacker_luck / (attacker_luck + 1.20 * defender_luck))

    base_chance = main_contribution * luck_ratio

    final_chance = base_chance * prod(multipliers) if multipliers else base_chance

    return max(0.01, min(0.75, final_chance))