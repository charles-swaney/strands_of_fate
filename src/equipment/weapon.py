from src.equipment.equipment import Equipment
from typing import Dict


class Weapon(Equipment):
    def __init__(
            self,
            name: str,
            slot: str,
            item_type: str,
            watk: int,
            wdef: int = 0,
            matk: int = 0,
            mdef: int = 0,
            element: str = None,
            equipment_stat_bonuses: Dict[str, int] = {}):
        self.name = name
        self._slot = slot
        self._item_type = item_type
        self._watk = watk
        self._wdef = wdef
        self._matk = matk
        self._mdef = mdef
        self.element = element
        self._equipment_stat_bonuses = equipment_stat_bonuses

    @property
    def equipment_stat_bonuses(self) -> Dict[str, int]:
        return self._equipment_stat_bonuses
    
    @property
    def slot(self) -> str:
        return self._slot
    
    @property
    def item_type(self) -> str:
        return self._item_type
    
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
