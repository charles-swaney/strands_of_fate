from typing import List
from actions.skill import Skill
from monsters.monster import Monster
from combat.compute_heal import compute_heal
from combat.compute_stat_buff import compute_stat_buff


class FaeBlessing(Skill):
    """
    Gives a minor heal to each ally, while simultaneously boosting their agility by a small
    amount.

    Monsters:
        - Fairy
    """
    def __init__(self):
        super().__init__(
            name="Fae Blessing",
            cost_type="mp",
            base_cost=12,
            cost_scaling=2,
            cooldown=5,
            magnitude=0.5,
            element=None,
            skill_type="heal"
        )
        self.target_type = "all"

    def execute(self,
                caster: Monster,
                targets: List[Monster],
                *other_multipliers) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        cost = self.cost(caster)

        caster.update_mp(-cost)

        multipliers = list(other_multipliers) + [self.magnitude]

        heal_value = 8 + compute_heal(caster=caster, multipliers=multipliers)
        stats_affected = ["agility"]

        for target in targets:

            target.update_hp(heal_value)

            bonus = compute_stat_buff(
                caster=caster,
                target=target,
                stats_affected=stats_affected,
                multipliers=multipliers
            )

            target.stat_buffs.update(bonus)

        self.remaining_cooldown = self._cooldown
