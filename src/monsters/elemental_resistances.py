from typing import Dict


class ElementalResistances:
    def __init__(self, resistances: Dict[str, float]):
        self.resistances = resistances

    def get_resistance(self, element: str) -> float:
        return self.resistances.get(element, 0)
    
    def set_resistance(self, element: str, new_value: float):
        self.resistances[element] = new_value
