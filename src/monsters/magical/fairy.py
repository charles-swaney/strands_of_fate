from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster
from ai.aggressive_ai import SingleTargetAggressiveAI


class Fairy(Monster):
    """
    A Fairy: an extremely quick and small monster known for its magical prowess and healing
    abilities.

    Growths:
        "hp": 4,
        "mp": 5,
        "strength": 1,
        "toughness": 2,
        "dexterity": 3,
        "agility": 9,
        "intellect": 9,
        "wisdom": 8,
        "speed": 9,
        "tenacity": 2,
        "charisma": 3,
        "luck": 6
    """
    def __init__(self, level = 1, aptitude = 5, deterministic = False, **stat_overrides):
        super().__init__(level, aptitude, deterministic, **stat_overrides)
        self.ai = SingleTargetAggressiveAI(owner=self)

    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 52
        return {
            "hp": 4,
            "mp": 5,
            "strength": 1,
            "toughness": 2,
            "dexterity": 3,
            "agility": 9,
            "intellect": 9,
            "wisdom": 8,
            "speed": 9,
            "tenacity": 2,
            "charisma": 3,
            "luck": 6
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": 1.50,
            "water": 0.75,
            "earth": 1.25,
            "wind": 0.50,
            "lightning": 1.00,
            "ice": 1.00,
            "light": 0.50,
            "dark": 1.50,
            "neutral": 1.00
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 1.00,
            "stab": 1.00,
            "blunt": 1.00,
            "ranged": 1.50,
            "misc": 1.25
        })

    @property
    def name(self) -> str:
        return "Fairy"

    @property
    def class_aptitude(self) -> int:
        return 1

    @property
    def watk(self) -> float:
        return self.base_watk

    @property
    def wdef(self) -> float:
        return self.base_wdef * 0.90

    @property
    def matk(self) -> float:
        return self.base_matk * 1.10

    @property
    def mdef(self) -> float:
        return self.base_mdef

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)
    
    @property
    def weapon_type(self):
        return "misc"
