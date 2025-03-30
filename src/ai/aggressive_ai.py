import random

from typing import Union, List
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from actions.action import Action
from ai.ai import AIBehavior


class AggressiveAI(AIBehavior):
    def do_action(self, battle: Battle):
        """
        Target selection for aggressive units. Aggressive units prioritize dealing damage to as
        many targets as possible, so if they an ability that targets multiple, they will use
        that. If not, they prefer to attack low hp units (but not deterministically).

        Target Priority:
            - If damage multiple skill available, then target multiple.
            - If debuff multiple skill available, then debuff multiple.
            - Otherwise, prefer to damage single target with low hp.
            - If no damage skill available, attack or debuff single target.
        """
        unit = self.owner

        opposing_side = battle.adventurers if isinstance(unit, Monster) else battle.monsters

        all_targets = [unit for unit in opposing_side if unit.hp > 0]
        if not all_targets:
            return

        unit_atk_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "damage"]
        unit_debuff_skills = [skill for skill in unit._all_known_skills if skill.skill_type == "debuff"]

        available_atk_skills = [skill for skill in unit_atk_skills if skill.can_be_used(unit)]
        available_debuff_skills = [skill for skill in unit_debuff_skills if skill.can_be_used(unit)]

        available_multi_atk_skills = [skill for skill in available_atk_skills if skill.target_type != "single"]
        available_multi_debuff_skills = [skill for skill in available_debuff_skills if skill.target_type != "single"]

        if len(all_targets) > 1:
            if available_multi_atk_skills:
                action_choice = random.choice(available_multi_atk_skills)
            elif available_debuff_skills:
                action_choice = random.choice(available_multi_debuff_skills)
            else:  # No multi attack or debuff skill available
                action_choice = None
            if action_choice:
                targets = all_targets if action_choice.target_type == "all" else random.sample(all_targets, min(2, len(all_targets)))
                unit.use(action_choice, targets)
                return action_choice.name, targets
        
        target = random.choice(all_targets)
        
        if target.hp / target.max_hp > 0.50:
            if available_atk_skills:
                action_choice = random.choice(available_atk_skills)
            elif available_debuff_skills:
                action_choice = random.choice(available_debuff_skills)
            else:
                unit.attack(target)
                print(f"Target is healthy, but no skills available. Attacked {target}")
                return "Attack", target
        else:  # Target has less than half hp
            if available_atk_skills:
                action_choice = random.choice(available_atk_skills)
            else:
                unit.attack(target)
                print(f"Target is weak, no attack skills. Attacked {target}.")
                return "Attack", target
        print(f"Using {action_choice} on {target}.")
        unit.use(action_choice, target)
        return action_choice.name, target
