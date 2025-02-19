from typing import Dict, Optional, List, TYPE_CHECKING
from core.stats.attributes import Attributes


if TYPE_CHECKING:
    from equipment.equipment import Equipment
    from jobs.job import Job


class EquipmentSlots:
    def __init__(self, valid_slots: Dict[str, List[str]]):
        """
        Initialize the equipment slots for some adventurer.

        Params:
            valid_slots: A dictionary whose keys are the equipment slot names
                (e.g. armor) and whose values are lists of valid equipment
                types (e.g. heavy_armor, light_armor, etc.)
        """
        self.valid_slots = valid_slots
        self.slots: Dict[str, Optional["Equipment"]] = {
            slot: None for slot in self.valid_slots
            }

    def equip(self, slot: str, item: Optional["Equipment"], job: "Job") -> None:
        """
        Equip a piece of equipment in the specified slot.

        Args:
            slot: the slot to equip the item to.
            item: the item to equip. Note: can be None to unequip in the specified slot.
            job: The adventurer's job (for class restrictions).
        """
        if slot not in self.valid_slots:
            raise ValueError(f"Invalid slot: {slot}")

        if item is not None:
            if item.slot != slot:
                raise ValueError(f"Cannot equip {item.item_type} in {slot} slot.")

            if item.item_type not in job.allowed_item_types[slot]:
                raise ValueError(f"{job.job_name}s cannot equip {item.item_type}.")

        self.slots[slot] = item

    def unequip(self, slot: str) -> None:
        """Unequip whatever is currently equipped in slot."""
        self.slots[slot] = None

    def get_item(self, slot: str) -> Optional["Equipment"]:
        """Return the item, if any, that is currently equipped in slot."""
        return self.slots.get(slot)

    def items(self) -> Dict[str, Optional["Equipment"]]:
        """Return all equipped items in a dictionary."""
        return self.slots.copy()

    def get_equipment_bonuses(self) -> "Attributes":
        """Return an Attributes object containing all equipment bonuses."""
        total_bonuses = Attributes({})
        for item in self.slots.values():
            if item is not None:
                item_bonuses = item.equipment_stat_bonuses
                total_bonuses.update(item_bonuses)
        return total_bonuses
