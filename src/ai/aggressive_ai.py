import random

from typing import Union, List
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from actions.action import Action
from ai.ai_behavior import AIBehavior
from ai.behavior_nodes.behavior_node import Selector
from ai.behavior_nodes.damage_skill_nodes import UseMultiTargetDamageSkill, UseDamageSkill, BasicAttackPreferLowHPTarget, BasicAttackRandomTarget
from ai.behavior_nodes.debuff_skill_nodes import UseMultiTargetDebuffSkill, UseDebuffSkill
from ai.behavior_nodes.buff_skill_nodes import UseMultiTargetBuffSkill, UseBuffSkill, UseSelfBuffSkill


class SmartAggressiveAI(AIBehavior):
    def __init__(self, owner):
        super().__init__(owner)
        
        self.behavior_tree = Selector([
            UseMultiTargetDamageSkill(),
            UseSelfBuffSkill(),
            UseMultiTargetDebuffSkill(),
            UseDamageSkill(),
            BasicAttackPreferLowHPTarget(),
            UseDebuffSkill(),
            UseBuffSkill(),
            BasicAttackRandomTarget()
        ])

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

        data = self.setup_data(battle=battle)

        self.behavior_tree.execute(unit, battle, data) 

        return data['result']
