from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.stats.attributes import Attributes


class Equipment(ABC):
    """Base equipment class."""

    @property
    @abstractmethod
    def equipment_stat_bonuses(self) -> "Attributes":
        """Returns an Attributes class containing the stats of the item."""
        pass
    
    @property
    @abstractmethod
    def watk(self) -> int:
        """Returns the item's watk."""
        pass
    
    @property
    @abstractmethod
    def wdef(self) -> int:
        """Return the item's wdef."""
        pass
    
    @property
    @abstractmethod
    def matk(self) -> int:
        """Return the item's matk."""
        pass
    
    @property
    @abstractmethod
    def mdef(self) -> int:
        """Return the item's mdef."""
        pass

    @property
    @abstractmethod
    def item_type(self) -> str:
        """Return the item's item type."""
        pass

    @property
    @abstractmethod
    def slot(self) -> str:
        """Return the slot where the item is supposed to be worn."""
        pass