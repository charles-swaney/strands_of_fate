from typing import List, Union
from actions.skill import Skill
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from combat.damage_calculator import compute_damage_physical
from combat.compute_heal import compute_heal_raw
from combat.hit_chance import compute_hit_chance
import random
import math


class Pair(Skill):
    def __init__(self):
        super().__init__(
            name="Pair",
            cost_type="mp",
            base_cost=10,
            cost_scaling=1.5,
            cooldown=2,
            magnitude=1.0,
            element=None,
            skill_type="damage"
        )
        self.target_type="dynamic"
    
    def execute(self,
                caster: Union[Adventurer, Monster],
                *other_multipliers) -> None:

        if not self.can_be_used(caster=caster):
            raise ValueError(f"Cannot cast {self.name}")
        
        if not isinstance(caster, Adventurer) or not (caster.job.job_name == "Gambler"):
            raise ValueError(f"Only Gamblers can cast {self.name}")
        
        cost = self.cost(caster=caster)

        caster.update_mp(-cost)

        numbers = [card[1] for card in caster.job.hand]
        pairs = [num for num in set(numbers) if numbers.count(num) >= 2]

        if not pairs:
            raise ValueError(f"Must have a pair to cast {self.name}")
        
        max_pair = max(pairs)

        paired_cards = [card for card in caster.job.hand if card[1] == max_pair]
        suits = [card[0] for card in paired_cards]

        if suits.count("spade") == 2:
            target_pair = None # TODO
            self._attack_twice(caster, target_pair, max_pair, *other_multipliers)
        elif suits.count("heart") == 2:
            target_pair = None # TODO
            self._heal_twice(caster, target_pair, max_pair, *other_multipliers)
        else:
            # Needs some logic for selecting a tuple of targets.
            target_pair = None # TODO
            self._attack_and_heal(caster, target_pair, max_pair, *other_multipliers)
        
        for card in paired_cards:
            caster.job.hand.remove(card)

        self.remaining_cooldown = self._cooldown

    def _attack_twice(self,
                      caster: Adventurer,
                      targets: Union[Adventurer, Monster, List[Adventurer], List[Monster], List[Adventurer, Monster]],
                      pair_value: int,
                      *other_multipliers) -> None:
        """
        Attacks twice. If only one enemy is available, attack them twice, with the second attack
        dealing reduced damage.
        """
        if len(targets) == 1:
            for target in targets:
                multiplier_1 = [self.magnitude, 1 + pair_value / 10] + list(other_multipliers)
                damage_1 = compute_damage_physical(caster,
                                                   target,
                                                   "standard",
                                                   caster.weapon_type,
                                                   multiplier_1)
                hit_chance = compute_hit_chance(caster, target)
                hit_roll = random.random()

                if hit_roll < hit_chance:
                    target.update_hp(-damage_1)
                multiplier_2 = multiplier_1 + [0.50]  # 50% reduced damage
                damage_2 = compute_damage_physical(caster,
                                                   target,
                                                   "standard",
                                                   caster.weapon_type,
                                                   multiplier_2)
                hit_chance = compute_hit_chance(caster, target)
                hit_roll = random.random()
                if hit_roll < hit_chance:
                    target.update_hp(-damage_2)
        else:
            for target in targets[:2]:
                multiplier = [self.magnitude]
                damage = compute_damage_physical(caster,
                                                   target,
                                                   "standard",
                                                   caster.weapon_type,
                                                   multiplier)
                hit_chance = compute_hit_chance(caster, target)
                hit_roll = random.random()

                if hit_roll < hit_chance:
                    target.update_hp(-damage)
    def _heal_twice(self,
                    caster: Adventurer,
                    targets: Union[Adventurer, List[Adventurer]],
                    pair_value: int,
                    *other_multipliers) -> None:
        """
        Heals twice. Can heal self. If only one ally alive (i.e., only Gambler alive), second
        heal has reduced effect.
        """
        multipliers = [self.magnitude, 1 + pair_value / 10] + list(other_multipliers)
        heal_amount = compute_heal_raw(caster.luck, multipliers=multipliers)
        if len(targets) == 1:
            for target in targets:
                target.update_hp(1.5 * heal_amount)  # Second heal has 50% effectiveness
        else:
            for target in targets[:2]:
                target.update_hp(heal_amount)
    
    def _attack_and_heal(self,
                         caster: Adventurer,
                         targets: tuple[Adventurer, Monster],
                         pair_value: int,
                         *other_multipliers) -> None:
        """
        Heal targets[0] for the heal amount, and attack targets[1] for the attack amount.
        """
        multipliers = [self.magnitude, 1 + pair_value / 10] + list(other_multipliers)

        heal_amount = compute_heal_raw(caster.luck, multipliers=multipliers)

        if not isinstance(targets[0], Adventurer) or not isinstance(targets[1], Monster):
            raise ValueError(f"Invalid target: {targets}")

        targets[0].update_hp(heal_amount)

        damage = compute_damage_physical(
            caster,
            targets[1],
            attack_type="standard",
            weapon_dmg_type=caster.weapon_type,
            multipliers=multipliers
        )

        hit_chance = compute_hit_chance(caster, targets[1])
        hit_roll = random.random()

        if hit_roll < hit_chance:
            targets[1].update_hp(-damage)


        
