from typing import Dict, TYPE_CHECKING
from utils.bonus_growth_calculations import compute_stat_bonus
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances

if TYPE_CHECKING:
    from monsters.monster import Monster


class Wolf(Monster):
    """
    A wolf.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 46
        return {
            "hp": 12,
            "mp": 2,
            "strength": 9,
            "toughness": 5,
            "dexterity": 6,
            "agility": 6,
            "intellect": 2,
            "wisdom": 3,
            "speed": 6,
            "tenacity": 4,
            "charisma": 1,
            "luck": 4
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": 1.0,
            "water": 1.0,
            "earth": 1.0,
            "wind": 1.0,
            "lightning": 1.0,
            "ice": 1.0,
            "light": 1.0,
            "dark": 1.0
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 1.25,
            "stab": 1.25,
            "blunt": 1.0,
            "ranged": 1.25,
            "misc": 1.0
        })

    @property
    def class_aptitude(self) -> int:
        return 0

    @property
    def species_name(self) -> str:
        return "Wolf"

    def apply_level_up(self, monster: "Monster") -> None:
        growth_rates = self.growth_rates

        for stat, growth_rate in growth_rates.items():
            if growth_rate <= 3:
                bonus_mult = 0.5
            elif growth_rate >= 4 and growth_rate <= 8:
                bonus_mult = 1
            else:
                bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=monster.aptitude,
                class_aptitude=self.class_aptitude
                )
            monster.stats.add_to_stat(
                stat,
                growth_rate + (bonus_mult * stat_bonus)
            )
