#!/bin/bash

MONSTER_SPECIES=$1
SUBDIR=$2

MONSTER_NAME=$(echo "$MONSTER_SPECIES" | sed -E 's/(^|_)([a-z])/\U\2/g')
LOWERCASE_MONSTER_NAME=$(echo "$MONSTER_SPECIES" | tr '[:upper:]' '[:lower:]')

OUTPUT_FILE="src/monsters/$SUBDIR/${LOWERCASE_MONSTER_NAME}.py"

cat <<EOF > "$OUTPUT_FILE"
from typing import Dict
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from monsters.monster import Monster


class $MONSTER_NAME(Monster):
    """
    A $MONSTER_NAME: Describe this monster.
    """
    @property
    def growth_rates(self) -> Dict[str, int]:
        # Total: TODO
        return {
            "hp": TODO,
            "mp": TODO,
            "strength": TODO,
            "toughness": TODO,
            "dexterity": TODO,
            "agility": TODO,
            "intellect": TODO,
            "wisdom": TODO,
            "speed": TODO,
            "tenacity": TODO,
            "charisma": TODO,
            "luck": TODO
        }

    @property
    def elemental_resistances(self) -> ElementalResistances:
        """Return the elemental resistances of this species."""
        return ElementalResistances({
            "fire": TODO,
            "water": TODO,
            "earth": TODO,
            "wind": TODO,
            "lightning": TODO,
            "ice": TODO,
            "light": TODO,
            "dark": TODO
        })

    @property
    def weapon_resistances(self) -> WeaponResistances:
        """Return the weapon type resistances of this species."""
        return WeaponResistances({
            "slash": TODO,
            "stab": TODO,
            "blunt": TODO,
            "ranged": TODO,
            "misc": TODO
        })

    @property
    def species_name(self) -> str:
        return "$MONSTER_SPECIES"

    @property
    def class_aptitude(self) -> int:
        return TODO

    def get_element_res(self, element: str) -> float:
        return self.elemental_resistances.get_resistance(element=element)

    def get_weapon_res(self, weapon_type: str) -> float:
        return self.weapon_resistances.get_resistance(weapon_type=weapon_type)
EOF
