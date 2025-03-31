from abc import ABC, abstractmethod
from typing import Union, Dict, List
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from actions.skill import Skill
from battles.battle_state import BattleState


class AIBehavior(ABC):
    def __init__(self, owner: Union[Adventurer, Monster]):
        self.owner = owner

    def setup_data(self, battle: Battle) -> BattleState:
        """
        Set up the data dictionary required by all the AI decision trees, according to the battle
        state and the unit's available skills.
        """
        unit = self.owner

        opposing_side = battle.adventurers if isinstance(unit, Monster) else battle.monsters
        allied_side = battle.monsters if isinstance(unit, Monster) else battle.adventurers
        all_enemies = [unit for unit in opposing_side if unit.hp > 0]
        all_allies = [unit for unit in allied_side if unit.hp > 0]

        if not all_enemies:
            return

        unit_dmg_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "damage"]
        unit_debuff_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "debuff"]
        unit_buff_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "buff"]
        unit_heal_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "heal"]

        available_dmg_skills = [skill for skill in unit_dmg_skills if skill.can_be_used(unit)]
        available_debuff_skills = [skill for skill in unit_debuff_skills if skill.can_be_used(unit)]
        available_buff_skills = [skill for skill in unit_buff_skills if skill.can_be_used(unit)]
        available_heal_skills = [skill for skill in unit_heal_skills if skill.can_be_used(unit)]

        available_multi_dmg_skills = [skill for skill in available_dmg_skills if skill.target_type != "single"]
        available_multi_debuff_skills = [skill for skill in available_debuff_skills if skill.target_type != "single"]
        available_multi_buff_skills = [skill for skill in available_buff_skills if skill.target_type != "single"]
        available_multi_heal_skills = [skill for skill in available_heal_skills if skill.target_type != "single"]

        data = {
            'all_enemies': all_enemies,
            'all_allies': all_allies,
            'available_dmg_skills': available_dmg_skills,
            'available_debuff_skills': available_debuff_skills,
            'available_buff_skills': available_buff_skills,
            'available_heal_skills': available_heal_skills,
            'available_multi_dmg_skills': available_multi_dmg_skills,
            'available_multi_debuff_skills': available_multi_debuff_skills,
            'available_multi_buff_skills': available_multi_buff_skills,
            'available_multi_heal_skills': available_multi_heal_skills,
            'result': None
        }

        return data

    @abstractmethod
    def do_action(self, unit: Union[Adventurer, Monster], battle: Battle):
        """
        Executes an action.
        """
        pass
