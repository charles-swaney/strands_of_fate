from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster


class Behemoth(Monster):
    """
    A Behemoth: A high-level monster that shrugs off most magic-based and physical attacks
    alike.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: 73
        return {
            "hp": 14,
            "mp": 4,
            "strength": 12,
            "toughness": 10,
            "dexterity": 6,
            "agility": 7,
            "intellect": 2,
            "wisdom": 7,
            "speed": 6,
            "tenacity": 14,
            "charisma": 2,
            "luck": 6
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": 0.75,
            "water": 0.75,
            "earth": 0.50,
            "wind": 1.00,
            "lightning": 0.75,
            "ice": 0.75,
            "light": 1.00,
            "dark": 0.50,
            "neutral": 0.75
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": 0.75,
            "stab": 0.75,
            "blunt": 1.00,
            "ranged": 0.75,
            "misc": 0.50
        })

    @property
    def species_name(self) -> str:
        return "Behemoth"

    @property
    def class_aptitude(self) -> int:
        return 1

    @property
    def watk(self) -> float:
        return self.base_watk

    @property
    def wdef(self) -> float:
        return self.base_wdef * 1.25

    @property
    def matk(self) -> float:
        return self.base_matk

    @property
    def mdef(self) -> float:
        return self.base_mdef * 1.25

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)

    @property
    def weapon_type(self):
        return "blunt"
