import pytest
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from jobs.mage_classes.black_mage import BlackMage
from jobs.warrior_classes.fighter import Fighter
from monsters.beasts.wolf import Wolf
from monsters.beasts.direwolf import DireWolf
from monsters.beasts.behemoth import Behemoth
from monsters.beasts.behemoth_skills import Trample, ExposeWeakness, IronHide, EarthenGrasp
from monsters.beasts.shared.aimed_strike import AimedStrike
from unittest.mock import patch


@pytest.fixture(autouse=True)
def patch_random_uniform():
    with patch("random.uniform", return_value=1.0):
        yield 

@pytest.fixture
def behemoth_():
    b = Behemoth(
        level=25,
        deterministic=True
    )
    return b

@pytest.fixture
def wolf_():
    w = Wolf(
        level=25,
        deterministic=True
    )
    return w

@pytest.fixture
def dwolf_():
    w = DireWolf(
        level=25,
        deterministic=True
    )
    return w

@pytest.fixture
def fighter_():
    f = Fighter()
    adv = Adventurer(
        name="Fighter",
        job=f,
        level=25,
        deterministic=True
    )
    return adv

@pytest.fixture
def blackmage_():
    bm = BlackMage()
    adv = Adventurer(
        name="BlackMage",
        job=bm,
        level=25,
        deterministic=True
    )
    return adv

def test_multi_available(behemoth_, wolf_, fighter_, blackmage_):
    behemoth, wolf, fighter, blackmage = behemoth_, wolf_, fighter_, blackmage_
    advs, monsters = [fighter, blackmage], [behemoth, wolf]
    trample = Trample()
    grasp = EarthenGrasp()
    ironhide = IronHide()
    battle = Battle(advs, monsters)
    behemoth.learn_skill(ironhide)
    behemoth.learn_skill(trample)
    behemoth.learn_skill(grasp)
    assert behemoth.do_action(battle)[0] == "Iron Hide"
    battle.tick_cooldowns()
    assert behemoth.do_action(battle)[0] == "Trample"
    battle.tick_cooldowns()
    assert behemoth.do_action(battle)[0] == "Attack"
    battle.tick_cooldowns()
    assert behemoth.do_action(battle)[0] == "Attack"
    battle.tick_cooldowns()


def test_multi_available(behemoth_, wolf_, dwolf_):
    behemoth, wolf, direwolf = behemoth_, wolf_, dwolf_
    advs, monsters = [wolf, direwolf], [behemoth]
    trample = Trample()
    grasp = EarthenGrasp()
    ironhide = IronHide()
    aimed_strike = AimedStrike()
    battle = Battle(advs, monsters)
    behemoth.learn_skill(ironhide)
    behemoth.learn_skill(trample)
    behemoth.learn_skill(grasp)
    wolf.learn_skill(aimed_strike)
    direwolf.learn_skill(aimed_strike)
    # R1
    print(direwolf.do_action(battle))
    # R2
    print(direwolf.do_action(battle))
    # R3
    print(direwolf.do_action(battle))
