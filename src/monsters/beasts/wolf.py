from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster


class Wolf(Monster):
    """
    A wolf: known for being agile, strong attackers with relatively weak defenses.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 46
        return {
            "hp": 11,
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
            "fire": 1.00,
            "water": 1.00,
            "earth": 1.00,
            "wind": 1.0,
            "lightning": 1.00,
            "ice": 1.00,
            "light": 1.00,
            "dark": 1.00
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 1.25,
            "stab": 1.25,
            "blunt": 1.00,
            "ranged": 1.25,
            "misc": 1.00
        })

    @property
    def species_name(self) -> str:
        return "Wolf"

    @property
    def class_aptitude(self) -> int:
        return 0

    @property
    def watk(self) -> float:
        return self.base_watk * 1.10

    @property
    def wdef(self) -> float:
        return self.base_wdef * 0.90

    @property
    def matk(self) -> float:
        return self.base_matk * 0.90

    @property
    def mdef(self) -> float:
        return self.base_mdef * 0.85

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)
