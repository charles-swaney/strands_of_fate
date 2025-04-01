import random
from typing import Dict, List, Union, Optional, Any
from battles.battle_state import BattleState
from battles.battle import Battle
from ai.behavior_nodes.behavior_node import BehaviorNode
from adventurers.adventurer import Adventurer
from monsters.monster import Monster


class UseMultiTargetDebuffSkill(BehaviorNode):
    """
    Attempt to use a skill that debuffs multiple targets.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])
        available_multi_debuff_skills = data.get("available_multi_debuff_skills", [])

        if not all_enemies or not available_multi_debuff_skills:
            return False

        if available_multi_debuff_skills and len(all_enemies) > 1:
            action_choice = random.choice(available_multi_debuff_skills)
            targets = all_enemies if action_choice.skill_type == 'all' else random.sample(all_enemies, 2)
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False


class UseDebuffSkill(BehaviorNode):
    """
    Attempt to use a skill that debuffs a single target.

    Note: this should typically occur after a check for `UseMultiTargetDebuffSkill`,
        as if there are multiple targets remaining, most Monsters should prioritize
        debuffing multiple. So this is usually executed only if there is only one enemy
        remaining. Despite this, the unit should use multi-target debuff skills if available.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get('all_enemies', [])
        available_debuff_skills = data.get('available_debuff_skills', [])

        if not all_enemies or not available_debuff_skills:
            return False

        if available_debuff_skills and all_enemies:
            action_choice = random.choice(available_debuff_skills)
            match action_choice.target_type:
                case "all": 
                    targets = all_enemies
                case "multiple":
                    targets = random.sample(all_enemies, 2)
                case "single":
                    targets = random.choice(all_enemies)
                case _:
                    raise ValueError(f"Invalid target type: {action_choice.target_type}.")
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False


class UseSingleDebuffSkillEarly(BehaviorNode):
    """
    Attempt to use a debuff skill, only if it is early on in the battle.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        available_debuff_skills = data.get('available_debuff_skills', [])
        single_debuffs = [debuff for debuff in available_debuff_skills if debuff.target_type == "single"]

        if single_debuffs:
            if battle.round_count <= 2:
                action_choice = random.choice(single_debuffs)
                target = unit
                unit.use(action_choice, target)
                data['result'] = (action_choice.name, target.name)
                return True
        return False
    