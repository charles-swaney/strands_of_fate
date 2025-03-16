from src.jobs.job import Job
from typing import Dict, TYPE_CHECKING, List
from utils.bonus_growth_calculations import compute_stat_bonus
from actions.gambler_attack import GamblerAttack

if TYPE_CHECKING:
    from src.jobs.job import Adventurer
    from src.jobs.job_requirements import StatRequirement, JobLevelRequirement


class Gambler(Job):
    """
    A class centered almost entirely around luck-based mechanics.

    Key Traits:
    - Incredible luck growth.
    - Extremely poor growth in magic-related skills, and extremely squishy overall.
    - Abilities range from damage-dealing, debuffing, and buffing allies,
        but always with a reliance random chance.
    - Unique minigame: 
        - A Gambler starts combat with an empty hand. Whenever they deal damage
        or heal allies, they add a card belonging to suit "spade" or "heart", respectively.
        The value of the card is the last digit of the damage they dealt, or the heal they
        applied.
        - Their abilities revolve around either adding additional cards to their hand on top
        of the guaranteed addition from dealing/healing damage, or using some set of cards from
        their hand to produce a special effect.
        - For example, their ability "Trick up the Sleeve" allows the unit to deal physical
        damage while drawing an additional card of random suit and value.


    Weapons:
    - Daggers

    Armor:
    - Light armor

    Growths:
        "hp": 4,
        "mp": 6,
        "strength": 6,
        "toughness": 3,
        "dexterity": 7,
        "agility": 7,
        "intellect": 2,
        "wisdom": 2,
        "speed": 7,
        "tenacity": 2,
        "charisma": 7,
        "luck": 11
    """

    def __init__(self):
        self._hand: List[tuple[str, int]] = []
        self._max_hand_size = 5

    @property
    def hand(self) -> List[tuple[str, int]]:
        """
        Returns the cards held in the current deck.

        Cards have the form: (suit, number), where suit is either 'heart' or 'spade', and
        number is an integer from 0-9.
        """
        return self._hand
    
    def add_card(self, suit: str, value: int) -> None:
        """
        Add a card to the hand if there is room in the hand, according to last digit of damage.
        """
        if len(self.hand) >= self._max_hand_size:
            return
        else:
            last_digit = abs(value) % 10
            suit = suit
            card = (suit, last_digit)
            self._hand.append(card)

    def reset_hand(self) -> None:
        """
        Reset the deck at the start of each battle.
        """
        self._hand = []

    def create_attack(self) -> GamblerAttack:
        return GamblerAttack()

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 55
        return {
            "hp": 4,
            "mp": 6,
            "strength": 6,
            "toughness": 3,
            "dexterity": 7,
            "agility": 7,
            "intellect": 2,
            "wisdom": 2,
            "speed": 7,
            "tenacity": 2,
            "charisma": 7,
            "luck": 11
        }

    @property
    def class_aptitude(self) -> int:
        return 0

    @property
    def job_name(self) -> str:
        return "Gambler"

    @property
    def allowed_item_types(self) -> Dict[str, List[str]]:
        return {
            "weapon": ["dagger"],
            "armor": ["light_armor"],
            "gauntlet": ["light_armor"],
            "greaves": ["light_armor"],
            "helmet": ["light_armor"],
            "accessory": ["ring", "necklace"],
            "shield": []
        }

    def stats_requirements(self) -> "StatRequirement":
        return StatRequirement({
            "agility": 80,
            "luck": 150  # Only the lucky can gamble !
        })

    def job_level_requirements(self) -> "JobLevelRequirement":
        return JobLevelRequirement({
            "Jester": 5,
            "Bard": 5
        })

    def apply_level_up(self, adventurer: "Adventurer") -> None:
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
            if adventurer.deterministic:
                bonus_mult = 0
            else:
                if growth_rate <= 3:
                    bonus_mult = 0.5
                elif growth_rate >= 4 and growth_rate <= 8:
                    bonus_mult = 1
                else:
                    bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=adventurer.aptitude,
                class_aptitude=self.class_aptitude
                )
            adventurer.base_stats.add_to_stat(
                stat,
                growth_rate + (bonus_mult * stat_bonus)
            )
