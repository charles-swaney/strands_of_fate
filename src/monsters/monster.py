from core.stats.attributes import Attributes
from typing import Dict, List, Union, TYPE_CHECKING
from monsters.elemental_resistances import ElementalResistances
from monsters.weapon_resistances import WeaponResistances
from abc import ABC, abstractmethod
from utils.bonus_growth_calculations import compute_stat_bonus


if TYPE_CHECKING:
    from actions.action import Action
    from adventurers.adventurer import Adventurer
    from actions.skill import Skill
    from combat.status_effects.status_effect import StatusEffect

class Monster(ABC):

    def __init__(
            self,
            level: int = 1,
            aptitude: float = 5,
            deterministic: bool = False,
            **stat_overrides: float):

        self.level = level
        self.aptitude = aptitude

        ZERO_STATS = {
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
        self._stat_buffs = Attributes(ZERO_STATS)

        from actions.attack import Attack
        self._attack = Attack()

        self._stats = Attributes(ZERO_STATS)
        self._all_known_skills = []
        self.deterministic = deterministic
        self._status_effects = []

        self.initialize_base_stats()

        for _ in range(2, self.level + 1):
            self.apply_level_up()

        self._stats.update_override(stat_overrides)
        self._hp = self.total_stats.get_stat("hp")
        self._mp = self.total_stats.get_stat("mp")

    @property
    def total_stats(self) -> Attributes:
        """Return the Attributes class containing the monster's stats."""
        total = self._stats.copy()
        total.update(self.stat_buffs)
        return total
    
    @property
    def stat_buffs(self) -> Attributes:
        """Return all stat buffs currently held by the unit."""
        return self._stat_buffs

    @property
    def max_hp(self) -> float:
        """Return the monster's max hp."""
        return self.total_stats.get_stat("hp")
    
    @property
    def max_mp(self) -> float:
        """Return the monster's max mp."""
        return self.total_stats.get_stat("mp")
    
    @property
    def hp(self) -> float:
        """Return the (current) hp."""
        return self._hp
    
    @hp.setter
    def hp(self, value):
        """Clamps hp between 0 and max hp"""
        self._hp = max(0, min(value, self.max_hp))

    @property
    def mp(self) -> float:
        """Return the (current) mp."""
        return self._mp
    
    @mp.setter
    def mp(self, value):
        """Clams mp between 0 and max mp."""
        self._mp = max(0, min(value, self.max_mp))

    @property
    def skills(self) -> List["Skill"]:
        """Return the list of known skills."""
        return self._all_known_skills
    
    def learn_skill(self, skill: "Skill") -> None:
        """Learn the skill, i.e., add it to known skills."""
        if skill not in self.skills:
            self._all_known_skills.append(skill)

    @property
    @abstractmethod
    def growth_rates(self) -> Dict[str, int]:
        """Return the growth rate of each stat for this species."""
        pass

    @property
    @abstractmethod
    def elemental_resistances(self) -> ElementalResistances:
        """Return elemental resistances (e.g., fire, ice)."""
        pass

    @property
    @abstractmethod
    def weapon_resistances(self) -> WeaponResistances:
        """Return resistances to various weapon types (e.g., slashing, piercing)."""
        pass

    @property
    @abstractmethod
    def species_name(self) -> str:
        """Return the name of the monster."""
        pass

    @property
    @abstractmethod
    def class_aptitude(self) -> float:
        """Return the monster's aptitude."""
        pass

    @property
    def base_watk(self) -> float:
        """
        Return the monster's base weapon attack. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        strength = self.get_total_stat("strength")
        luck = self.get_total_stat("luck")
        return (1.0 * strength + 0.03 * luck)

    @property
    def base_wdef(self) -> float:
        """
        Return the monster's base weapon defense. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        toughness = self.get_total_stat("toughness")
        luck = self.get_total_stat("luck")
        return (1.0 * toughness + 0.03 * luck)

    @property
    def base_matk(self) -> float:
        """
        Return the monster's base magic attack. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        intellect = self.get_total_stat("intellect")
        charisma = self.get_total_stat("charisma")
        luck = self.get_total_stat("luck")
        return (1.08 * intellect + 0.03 * luck)

    @property
    def base_mdef(self) -> float:
        """
        Return the monster's base magic defense. Can be affected by monster-specific bonuses which
        are handled within the species implementation.
        """
        wisdom = self.get_total_stat("wisdom")
        tenacity = self.get_total_stat("tenacity")
        luck = self.get_total_stat("luck")
        return (1.0 * wisdom +
                0.15 * tenacity +
                0.03 * luck)

    @property
    @abstractmethod
    def watk(self) -> float:
        """Total weapon attack, including bonuses."""
        pass

    @property
    @abstractmethod
    def wdef(self) -> float:
        """Total weapon defense, including bonuses."""
        pass

    @property
    @abstractmethod
    def matk(self) -> float:
        """Total magic attack, including bonuses."""
        pass

    @property
    @abstractmethod
    def mdef(self) -> float:
        """Total magic defense, including bonuses."""
        pass

    @abstractmethod
    def get_element_res(self, element: str) -> float:
        """Return the monster's resistance to element."""
        pass

    @abstractmethod
    def get_weapon_res(self, weapon_type: str) -> float:
        """Return the monster's resistance to weapon_type."""
        pass

    @property
    @abstractmethod
    def weapon_type(self) -> str:
        """Return the monster's weapon type."""
        pass

    def level_up(self):
        """Increase Monster level and apply stat growths."""
        self.level += 1
        self.apply_level_up()

    def get_total_stat(self, stat: str) -> float:
        """Return stat."""
        return self.total_stats.get_stat(stat)

    def initialize_base_stats(self):
        """Apply level up without incrementing level."""
        self.apply_level_up()
        base_hp = self.total_stats.get_stat("hp")
        base_mp = self.total_stats.get_stat("mp")
        self._stats.update(Attributes(
            {
                "hp": 3 * base_hp,
                "mp": 3 * base_mp
            }
        ))

    def apply_level_up(self) -> None:
        """Level up the monster, based on growth rates and aptitude."""
        growth_rates = self.growth_rates
        for stat, growth_rate in growth_rates.items():
            if self.deterministic:
                bonus_mult = 0
            else:
                if growth_rate <= 3:
                    bonus_mult = 0.5
                elif growth_rate >= 4 and growth_rate <= 8:
                    bonus_mult = 1.0
                else:
                    bonus_mult = 1.5
            stat_bonus = compute_stat_bonus(
                base_aptitude=self.aptitude,
                class_aptitude=self.class_aptitude
            )
            self._stats.add_to_stat(stat, growth_rate + (bonus_mult * stat_bonus))

    def update_hp(self, amount: float) -> None:
        """A flexible health update to support either healing or taking damage."""
        self.hp += amount

    def update_mp(self, amount: float) -> None:
        """A flexible mana update to support either casting, or having mana replenished."""
        self.mp += amount

    def status_effects(self) -> List["StatusEffect"]:
        return self._status_effects
    
    def attack(self, target):
        self._attack.execute(self, [target])

    def can_access(self, skill: "Action") -> bool:
        """Return whether skill can be accessed."""
        return skill in self.skills
    
    def use(self, skill: "Action",
            targets: Union["Adventurer", "Monster", List["Adventurer"], List["Monster"]]):
        """Cast skill on targets."""
        from adventurers.adventurer import Adventurer
        if isinstance(targets, Adventurer) or isinstance(targets, Monster):
            skill.execute(caster=self, 
                          targets=[targets])
        else:
            skill.execute(caster=self,
                          targets=targets)
