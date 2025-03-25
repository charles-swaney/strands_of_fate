from typing import List, Union
from actions.skill import Skill
from monsters.monster import Monster
from adventurers.adventurer import Adventurer
from combat.compute_heal import compute_heal_raw


class UnyieldingWill(Skill):
    def __init__(self):
        """
        Heals the unit based on their tenacity, with a bonus based on missing health, up to 50%.
        Also shakes off all status effects (good and bad), but temporarily lowers the unit's
        strength and intellect.

        Monsters:
            - Behemoth

        Classes:
            - Guardian
        """
        super().__init__(
            name="Unyielding Will",
            cost_type="mp",
            base_cost=12,
            cost_scaling=1.75,
            cooldown=5,
            magnitude=0.75,
            element=None,
            skill_type="buff"
        )
        self.target_type="self"

    def execute(self,
                caster: Union[Adventurer, Monster],
                targets: Union[List[Adventurer], List[Monster]],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")
        
        cost = self.cost(caster)

        caster.update_mp(-cost)

        for target in targets:
            target.status_effects = []
            strength_penalty = target.strength * 0.25
            intellect_penalty = target.intellect * 0.25

            heal_value = caster.tenacity
            hp_proportion = caster.hp / caster.max_hp
            missing_hp_bonus = 1 + (1 - hp_proportion) / 2

            heal_base = compute_heal_raw(
                heal_value=heal_value,
                multipliers=[self.magnitude] + list(other_multipliers) + [missing_hp_bonus]
            )
            target.hp += heal_base

            target.stat_buffs.update(
                {
                    "strength": -strength_penalty,
                    "intellect": -intellect_penalty
                }
            )

        self.remaining_cooldown = self._cooldown
