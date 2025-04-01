import random
from typing import Dict, List, Union, Optional, Any
from battles.battle_state import BattleState
from battles.battle import Battle
from ai.behavior_nodes.behavior_node import BehaviorNode
from adventurers.adventurer import Adventurer
from monsters.monster import Monster


class UseMultiTargetBuffSkill(BehaviorNode):
    """
    Use a skill that buffs multiple targets.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_allies = data.get("all_allies", [])
        available_multi_buff_skills = data.get("available_multi_buff_skills", [])

        if not all_allies or not available_multi_buff_skills:
            return False

        if available_multi_buff_skills and len(all_allies) > 1:
            action_choice = random.choice(available_multi_buff_skills)
            targets = all_allies if action_choice.skill_type == 'all' else random.sample(all_allies, 2)
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False


class UseBuffSkill(BehaviorNode):
    """
    Use a skill that buffs a single target.

    Note: this should typically occur after a check for `UseMultiTargetBuffSkill`,
        as if there are multiple allies remaining, most Monsters should prioritize
        buffing multiple. So this is usually executed only if there is only one ally
        remaining. Despite this, the unit should use multi-target buff skills if available.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_allies = data.get('all_allies', [])
        available_buff_skills = data.get('all_buff_skills', [])

        if not all_allies or not available_buff_skills:
            return False

        if available_buff_skills and all_allies:
            action_choice = random.choice(available_buff_skills)
            match action_choice.target_type:
                case "all": 
                    targets = all_allies
                case "multiple":
                    targets = random.sample(all_allies, 2)
                case "single":
                    targets = random.choice(all_allies)
                case _:
                    raise ValueError(f"Invalid target type: {action_choice.target_type}.")
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False
    

class UseSelfBuffSkillEarly(BehaviorNode):
    """
    Use a skill that buffs the caster, only if it is early on in the battle.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        available_buff_skills = data.get('available_buff_skills', [])
        self_buffs = [buff for buff in available_buff_skills if buff.target_type == "self"]

        if self_buffs:
            if battle.round_count <= 2:
                action_choice = random.choice(self_buffs)
                target = unit
                unit.use(action_choice, target)
                data['result'] = (action_choice.name, target.name)
                return True
        return False
    

class UseSelfBuffSkill(BehaviorNode):
    """
    Use a skill that buffs the caster.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        available_buff_skills = data.get('available_buff_skills', [])
        self_buffs = [buff for buff in available_buff_skills if buff.target_type == "self"]

        if self_buffs:
            action_choice = random.choice(self_buffs)
            target = unit
            unit.use(action_choice, target)
            data['result'] = (action_choice.name, target.name)
            return True
        return False
