import random

from typing import Union, List
from battles.battle import Battle
from actions.action import Action
from ai.ai_behavior import AIBehavior
from ai.behavior_nodes.behavior_node import Selector
from ai.behavior_nodes.damage_skill_nodes import UseMultiTargetDamageSkill, UseDamageSkill, BasicAttackPreferLowHPTarget, BasicAttackRandomTarget, BasicAttackLowestHPTarget
from ai.behavior_nodes.debuff_skill_nodes import UseMultiTargetDebuffSkill, UseDebuffSkill
from ai.behavior_nodes.buff_skill_nodes import UseMultiTargetBuffSkill, UseBuffSkill, UseSelfBuffSkillEarly


class AoEAggressiveAI(AIBehavior):
    def __init__(self, owner):
        """
        Action selection for AoE aggressive units. Aggressive units prioritize dealing damage to as
        many targets as possible, so if they an ability that targets multiple, they will use
        that. If not, they prefer to attack low hp units (but not deterministically).

        Action Priority:
            - If early in combat, buff self.
            - Use a multi-target damage ability.
            - Use a multi-target debuff ability.
            - Use a single-target damage ability.
            - Basic attack a single target with low hp.
            - Use a single-trget debuff.
            - Basic attack a random target.
        """
        super().__init__(owner)
        
        self.behavior_tree = Selector([
            UseSelfBuffSkillEarly(),
            UseMultiTargetDamageSkill(),
            UseMultiTargetDebuffSkill(),
            UseDamageSkill(),
            BasicAttackPreferLowHPTarget(),
            UseDebuffSkill(),
            UseBuffSkill(),
            BasicAttackRandomTarget()
        ])

    def do_action(self, battle: Battle):
        unit = self.owner

        data = self.setup_data(battle=battle)

        self.behavior_tree.execute(unit, battle, data) 

        return data['result']


class SingleTargetAggressiveAI(AIBehavior):
    def __init__(self, owner):
        """
        Action selection for Single Target-Focused Aggressive Units. These units prioritize
        dealing single-target damage. They are less "inclined" to use AoE abilities, but make up
        for this deficiency with smarter targetting of low-hp targets.

        Action Priority:
            - If there is a target whose hp is below 50%, attack them.
            - Use a single-unit targetting damage ability.
            - Use an AoE damage ability.
            - Attack a random target.
            - Use an AoE debuff ability.
            - Use a single-target debuff ability.
        """
        super().__init__(owner)

        self.behavior_tree = Selector([
            UseDamageSkill(),
            BasicAttackLowestHPTarget(),
            UseMultiTargetDamageSkill(),
            BasicAttackRandomTarget(),
            UseMultiTargetDebuffSkill(),
            UseDebuffSkill()
        ])

    def do_action(self, battle: Battle):
        unit = self.owner

        data = self.setup_data(battle=battle)

        self.behavior_tree.execute(unit, battle, data) 

        return data['result']
    

class DumbAggressiveAI(AIBehavior):
    def __init__(self, owner):
        """
        Action selection for Dumb Aggressive Units. These units do not have good action
        prioritization, and their basic attacks are always random, even if they have the chance
        to potentially finish off a weak enemy.

        Action Priority:
            - Use any damage skill.
            - Use any multi-target damage skill.
            - Use any multi-target debuff skill.
            - Use any debuff skill.
            - Attack a random target.
        """
        super().__init__(owner)

        self.behavior_tree = Selector([
            UseDamageSkill(),
            UseMultiTargetDamageSkill(),
            UseMultiTargetDebuffSkill(),
            UseDebuffSkill(),
            BasicAttackRandomTarget(),
        ])

    def do_action(self, battle: Battle):
        unit = self.owner

        data = self.setup_data(battle=battle)

        self.behavior_tree.execute(unit, battle, data) 

        return data['result']
