from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster


class Boar(Monster):
    """
    A Boar: A wild animal that is unpredictable, but strong and tough. Somewhat weak to magic.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 44
        return {
            "hp": 14,
            "mp": 2,
            "strength": 8,
            "toughness": 8,
            "dexterity": 3,
            "agility": 3,
            "intellect": 2,
            "wisdom": 2,
            "speed": 4,
            "tenacity": 7,
            "charisma": 2,
            "luck": 5
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": 1.25,
            "water": 1.00,
            "earth": 0.75,
            "wind": 1.50,
            "lightning": 1.25,
            "ice": 1.25,
            "light": 1.00,
            "dark": 1.00
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 0.75,
            "stab": 1.25,
            "blunt": 1.00,
            "ranged": 1.25,
            "misc": 1.00
        })

    @property
    def species_name(self) -> str:
        return "Boar"

    @property
    def class_aptitude(self) -> int:
        return 0.5

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)
