import random
from typing import Dict, List, Union, Optional, Any
from battles.battle_state import BattleState
from battles.battle import Battle
from ai.behavior_nodes.behavior_node import BehaviorNode
from adventurers.adventurer import Adventurer
from monsters.monster import Monster


class UseMultiTargetDamageSkill(BehaviorNode):
    """
    Attempt to use a skill that damages multiple targets. 
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])
        available_multi_dmg_skills = data.get("available_multi_dmg_skills", [])
        if not all_enemies or not available_multi_dmg_skills:
            return False

        # Not sure if I need to check len(all_enemies) > 1.
        if available_multi_dmg_skills and len(all_enemies) > 1:
            action_choice = random.choice(available_multi_dmg_skills)
            targets = all_enemies if action_choice.skill_type == 'all' else random.sample(all_enemies, 2)
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False
    

class UseDamageSkill(BehaviorNode):
    """
    Attempt to use a skill that damages a single target. 
    
    Note: this should typically occur after a check for `UseMultiTargetDamageSkill`,
        as if there are multiple targets remaining, most Monsters should prioritize
        damaging multiple. So this is usually executed only if there is only one enemy
        remaining. Despite this, the unit should use multi-target damage skills if available.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])
        available_damage_skills = data.get("available_dmg_skills", [])

        if not all_enemies or not available_damage_skills:
            return False

        if available_damage_skills and all_enemies:
            action_choice = random.choice(available_damage_skills)
            match action_choice.target_type:
                case "all": 
                    targets = all_enemies
                case "multiple":
                    targets = random.sample(all_enemies, 2)
                case "single":
                    targets = [random.choice(all_enemies)]
                case _:
                    raise ValueError(f"Invalid target type: {action_choice.target_type}.")
            unit.use(action_choice, targets)
            target_name = [target.name for target in targets]
            if len(target_name) == 1:
                target_name = target_name[0]
            data['result'] = (action_choice.name, target_name)
            return True
        return False


class BasicAttackLowestHPTarget(BehaviorNode):
    """
    Attempt to basic attack the target with the lowest proportion of remaining hp.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])
        
        if not all_enemies:
            return False
        
        targets_by_hp = sorted(all_enemies, key = lambda e: e.hp / e.max_hp)

        if targets_by_hp and (targets_by_hp[0].hp <= 0.50):
            target = targets_by_hp[0]
            unit.attack(target)
            data['result'] = ("Attack", target.name)
            return True
        return False


class BasicAttackRandomTarget(BehaviorNode):
    """
    Attempt to basic attack a random target.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])

        if not all_enemies:
            return False

        if all_enemies:
            target = random.choice(all_enemies)
            unit.attack(target)
            data['result'] = ("Attack", target.name)
            return True
        return False
    

class BasicAttackPreferLowHPTarget(BehaviorNode):
    """
    Attempt to basic attack a semi-random target, with probability weights distributed according
    to targets' proportion of max hp remaining.
    """
    def execute(self, unit: Union[Adventurer, Monster], battle: Battle, data: Optional[BattleState]):
        all_enemies = data.get("all_enemies", [])

        if not all_enemies:
            return False

        hp_ratios = [1.5 - (enemy.hp / enemy.max_hp) for enemy in all_enemies]

        weights = [hp_ratio / sum(hp_ratios) for hp_ratio in hp_ratios]
        targets_by_hp = sorted(all_enemies, key = lambda e: e.hp / e.max_hp)

        if all_enemies and (targets_by_hp[0].hp <= 0.50):
            target = random.choices(population=all_enemies, weights=weights)[0]
            unit.attack(target)
            data['result'] = ("Attack", target.name)
            return True
        return False
