from typing import Optional, Dict, Union, TYPE_CHECKING, List
from collections import defaultdict
from src.core.stats.attributes import Attributes
from equipment.equipment_slots import EquipmentSlots
from equipment.equipment import Equipment
from equipment.weapon import Weapon
from monsters.monster import Monster

if TYPE_CHECKING:
    from src.jobs.job import Job
    from actions.action import Action
    from actions.spell import Spell
    from combat.status_effects.status_effect import StatusEffect

class Adventurer:

    def __init__(
            self,
            name: str,
            job: "Job",
            level: int = 1,
            levels_gained: Optional[Union[Dict[str, int], defaultdict]] = None,
            aptitude: float = 5,
            deterministic: bool = False,
            **stat_overrides: float):
        
        self.name = name
        self.job = job
        self.level = level
        self.deterministic = deterministic
        self._status_effects = []
        self.levels_gained: defaultdict[str, int] = defaultdict(int)

        if isinstance(levels_gained, dict):
            self.levels_gained.update(levels_gained)
        elif isinstance(levels_gained, defaultdict):
            self.levels_gained = levels_gained.copy()
        self.aptitude = aptitude

        base_stats = {
            "hp": 0,
            "mp": 0,
            "strength": 0,
            "toughness": 0,
            "dexterity": 0,
            "agility": 0,
            "intellect": 0,
            "wisdom": 0,
            "speed": 0,
            "tenacity": 0,
            "charisma": 0,
            "luck": 0,
        }
        self._base_stats = Attributes(base_stats)

        self._equipment = EquipmentSlots(valid_slots=self.job.allowed_item_types)
        
        self.initialize_base_stats()

        for _ in range(2, self.level + 1):
            self.job.apply_level_up(self)

        self._hp = self.total_stats.get_stat("hp")
        self._mp = self.total_stats.get_stat("mp")

        from actions.attack import Attack
        self._attack = Attack()

        self._all_known_skills = defaultdict(list)

        from core.skillsets.skillset import Skillset
        self._skillset = Skillset(all_skills=self._all_known_skills,
                                  primary_job=self.job.job_name,
                                  secondary_job=None,
                                  passive=None)

        self._base_stats.update_override(stat_overrides)

    @property
    def base_stats(self) -> Attributes:
        """Base stats without equipment or other bonuses."""
        return self._base_stats

    @property
    def equipment_bonuses(self) -> Attributes:
        """Stat bonuses from all equipment."""
        return self.equipment.get_equipment_bonuses()

    @property
    def total_stats(self) -> Attributes:
        """Total stats from base stats, equipment, and other bonuses."""
        total = self._base_stats.copy()
        total.update(self.equipment_bonuses)
        return total

    @property
    def skills(self) -> Dict[str, List["Action"]]:
        """Return the list of known skills within each class.   """
        return self._all_known_skills
    
    @property
    def skillset(self):
        """Return the current skillset."""
        return self._skillset
    
    def learn_skill(self, skill: "Action") -> None:
        """Learn the spell."""
        current_job = self.job.job_name
        if skill not in self.skillset.primary_skillset:
            self.skillset.primary_skillset.append(skill)
        if skill not in self._all_known_skills[current_job]:
            self._all_known_skills[current_job].append(skill)

    @property
    def equipment(self) -> EquipmentSlots:
        return self._equipment
    
    @property
    def hp(self) -> float:
        """Return the (current) hp."""
        return self._hp
    
    @hp.setter
    def hp(self, value):
        """Clamps hp between 0 and max hp."""
        self._hp = max(0, min(value, self.total_stats.get_stat("hp")))

    @property
    def mp(self) -> float:
        """Return the (current) mp."""
        return self._mp
    
    @mp.setter
    def mp(self, value):
        """Clamps mp between 0 and max mp."""
        self._mp = max(0, min(value, self.total_stats.get_stat("mp")))

    @property
    def watk(self) -> float:
        """Damage dealt when attacking with a weapon."""
        base = (1.0 * self.get_total_stat("strength") +
                0.03 * self.get_total_stat("luck"))
        equipment_watk = self.get_equipment_combat_stat('watk')
        return base + equipment_watk

    @property
    def wdef(self) -> float:
        """Resistance to physical damage."""
        base = (1.0 * self.get_total_stat("toughness") +
                0.03 * self.get_total_stat("luck"))
        equipment_wdef = self.get_equipment_combat_stat('wdef')
        return base + equipment_wdef

    @property
    def matk(self) -> float:
        """Damage dealt with spells."""
        base = (1.08 * self.get_total_stat("intellect") +
                0.03 * self.get_total_stat("luck"))
        equipment_matk = self.get_equipment_combat_stat('matk')
        return base + equipment_matk

    @property
    def mdef(self) -> float:
        """Resistence to magical damage."""
        base = (self.get_total_stat("wisdom") +
                0.15 * self.get_total_stat("tenacity") +
                0.03 * self.get_total_stat("luck"))
        equipment_mdef = self.get_equipment_combat_stat('mdef')
        return base + equipment_mdef
    
    def get_equipment_combat_stat(self, stat: str) -> float:
        """Return the total combat stat (e.g. matk, wdef) from all equipment."""
        stat_total = sum(
            getattr(equipment, stat) for equipment in self.equipment.slots.values() if
            equipment is not None
        )
        return stat_total

    def get_base_stat(self, stat: str) -> float:
        """Conveniently return the base stat."""
        return self.base_stats.get_stat(stat)

    def get_total_stat(self, stat: str) -> float:
        """Conveniently return the total stat."""
        return self.total_stats.get_stat(stat)

    def equip(self, slot, item: Equipment):
        """Equip the given item in slot and update stats."""
        self.equipment.equip(slot, item, self.job)

    def unequip(self, slot: str):
        """Unequip whatever is equipped in slot and update stats."""
        self.equipment.unequip(slot)

    def _add_level_gained(self) -> None:
        """Log a level up within the Adventurer's current class."""
        self.levels_gained[self.job.job_name] += 1

    def initialize_base_stats(self) -> None:
        """Initialize adventurer with base stats."""
        self.job.apply_level_up(self)
        base_hp = self.base_stats.get_stat("hp")
        base_mp = self.base_stats.get_stat("mp")
        self._base_stats.update(Attributes(
            {
            "hp": 3 * base_hp,
            "mp": 3 * base_mp
            }
        ))

    def level_up(self):
        """Increase Adventurer level with stat growths and log level gained."""
        self.level += 1
        self.job.apply_level_up(self)
        self._add_level_gained()

    def update_hp(self, amount: float) -> None:
        """A flexible health update to support either healing or taking damage."""
        self.hp += amount

    def update_mp(self, amount: float) -> None:
        """A flexible mana update to support either casting, or having mana replenished."""
        self.mp += amount

    @property
    def equipped_weapon(self) -> Optional[Weapon]:
        """Return the equipped weapon, if any."""
        return self.equipment.get_item("weapon")

    @property
    def weapon_type(self) -> str:
        """Return the weapon type of the weapon the adventurer has equipped."""
        if not self.equipped_weapon:
            return "blunt"
        else:
            return self.equipped_weapon.damage_type
        
    def status_effects(self) -> List["StatusEffect"]:
        """Return the list of StatusEffects."""
        return self._status_effects
    
    def attack(self, target):
        self._attack.execute(self, [target])

    def can_access(self, skill: "Action") -> bool:
        """Return whether skill can be cast."""
        # First check if it's one of the primary or secondary skills.
        if skill in self.skillset.primary_skillset or \
            skill in self.skillset.secondary_skillset:
            return True
        return False
    
    def use(self, skill: "Action", targets: Union[Union["Adventurer", Monster], List[Union["Adventurer", Monster]]]) -> None:
        """Cast skill on target."""
        from monsters.monster import Monster
        if isinstance(targets, Adventurer) or isinstance(targets, Monster):
            skill.execute(self, [targets])
        else:
            skill.execute(self, targets)

    def compute_max_hp(self):
        return self.base_stats.get
