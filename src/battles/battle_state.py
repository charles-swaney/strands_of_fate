from typing import TypedDict, Union, List
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from actions.skill import Skill

class BattleState(TypedDict):
    all_enemies: Union[List[Adventurer], List[Monster]]
    all_allies: Union[List[Adventurer], List[Monster]]
    available_dmg_skills: List[Skill]
    available_debuff_skills: List[Skill]
    available_buff_skills: List[Skill]
    available_heal_skills: List[Skill]
    available_multi_dmg_skills: List[Skill]
    available_multi_debuff_skills: List[Skill]
    available_multi_buff_skills: List[Skill]
    available_multi_heal_skills: List[Skill]
    result: None
