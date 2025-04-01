from typing import List
from actions.skill import Skill
from monsters.monster import Monster
from combat.compute_stat_buff import compute_stat_buff


class MischievousMirage(Skill):
    def __init__(self):
        """
        Raises the unit's agility, speed, and luck temporarily.

        Monsters:
            - Fairy
        """
        super().__init__(
            name="Mischievous Mirage",
            cost_type="mp",
            base_cost=12,
            cost_scaling=1.75,
            cooldown=5,
            magnitude=0.75,
            element="neutral",
            skill_type="buff"
        )
        self.target_type = "self"

    def execute(self,
                caster: Monster,
                targets: List[Monster]) -> None:

        if not self.can_be_used(caster):
            raise ValueError(f"Cannot cast {self.name}.")

        cost = self.cost(caster)

        caster.update_mp(-cost)
        stats_affected = ["agility", "speed", "luck"]

        for target in targets:
            bonus = compute_stat_buff(
                caster=caster,
                target=caster,
                stats_affected=stats_affected
            )

            caster.total_stats.update(bonus)

        self.remaining_cooldown = self._cooldown

    def can_be_used(self, caster: Monster):
        cost = self.cost(caster)
        if caster.mp < cost:
            return False
        if self.remaining_cooldown > 0:
            return False
        return True
