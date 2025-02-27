from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster


class DireWolf(Monster):
    """
    A Dire Wolf: the natural evolution of a Wolf.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 61
        return {
            "hp": 12,
            "mp": 3,
            "strength": 11,
            "toughness": 6,
            "dexterity": 8,
            "agility": 8,
            "intellect": 3,
            "wisdom": 4,
            "speed": 8,
            "tenacity": 5,
            "charisma": 2,
            "luck": 6
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": 1.00,
            "water": 1.00,
            "earth": 1.00,
            "wind": 1.00,
            "lightning": 0.75,
            "ice": 0.75,
            "light": 1.00,
            "dark": 1.00
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 1.00,
            "stab": 1.00,
            "blunt": 1.00,
            "ranged": 1.25,
            "misc": 1.00
        })

    @property
    def species_name(self) -> str:
        return "DireWolf"

    @property
    def class_aptitude(self) -> int:
        return 0.5

    @property
    def watk(self) -> float:
        return self.base_watk * 1.10

    @property
    def wdef(self) -> float:
        return self.base_wdef

    @property
    def matk(self) -> float:
        return self.base_matk

    @property
    def mdef(self) -> float:
        return self.base_mdef * 0.85

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)
    
    def weapon_type(self):
        return "slash"
