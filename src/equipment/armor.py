from src.equipment.equipment import Equipment
from typing import Dict


class Armor(Equipment):
    def __init__(
            self,
            name: str,
            armor_type: str,
            wdef: int,
            mdef: int,
            matk: int = 0,
            watk: int = 0,
            equipment_stat_bonuses: Dict[str, int] = {}):
        self.name = name
        self.type = type
        self._watk = watk
        self._wdef = wdef
        self._matk = matk
        self._mdef = mdef
        self._equipment_stat_bonuses = equipment_stat_bonuses

    @property
    def equipment_stat_bonuses(self) -> Dict[str, int]:
        return self._equipment_stat_bonuses
    
    @property
    def watk(self) -> int:
        return self._watk
    
    @property
    def wdef(self) -> int:
        return self._wdef
    
    @property
    def matk(self) -> int:
        return self._matk
    
    @property
    def mdef(self) -> int:
        return self._mdef
    