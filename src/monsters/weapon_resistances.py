from typing import Dict


class WeaponResistances:
    def __init__(self, resistances: Dict[str, float]):
        self.resistances = resistances

    def get_resistance(self, weapon_type: str) -> float:
        return self.resistances.get(weapon_type, 0)
    
    def set_resistance(self, weapon_type: str, new_value: float):
        self.resistances[weapon_type] = new_value
