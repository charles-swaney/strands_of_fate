from actions.attack import Attack
from typing import List, Union, TYPE_CHECKING
from combat.damage_calculator import compute_damage_physical
import math

if TYPE_CHECKING:
    from adventurers.adventurer import Adventurer
    from monsters.monster import Monster

class GamblerAttack(Attack):
    """A Gambler-specific attack that updates their deck based on damage dealt."""

    def execute(self,
                attacker: Union["Adventurer", "Monster"],
                targets: List[Union["Adventurer", "Monster"]]) -> None:
        damage_values = super().execute(attacker, targets)

        if hasattr(attacker, "job") and attacker.job.job_name == "Gambler":
            for damage in damage_values:
                if damage > 0:
                    attacker.job.add_card(suit="spade", value=math.floor(damage))
