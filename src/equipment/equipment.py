from abc import ABC, abstractmethod
from typing import Dict, Optional

class Equipment(ABC):
    """
    Base Equipment class.
    """
    @property
    @abstractmethod
    def equipment_stat_bonuses(self) -> Dict[str, int]:
        """
        Returns a dictionary of stat bonuses applied by the Equipment.
        """
        pass
    
    @property
    @abstractmethod
    def watk(self) -> int:
        pass
    
    @property
    @abstractmethod
    def wdef(self) -> int:
        pass
    
    @property
    @abstractmethod
    def matk(self) -> int:
        pass
    
    @property
    @abstractmethod
    def mdef(self) -> int:
        pass