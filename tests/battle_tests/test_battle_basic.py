import pytest
from battles.battle import Battle
from adventurers.adventurer import Adventurer
from monsters.monster import Monster
from jobs.mage_classes.black_mage import BlackMage
from jobs.warrior_classes.fighter import Fighter
from monsters.beasts.wolf import Wolf
from monsters.beasts.behemoth import Behemoth
from monsters.beasts.behemoth_skills import Trample
from pytest import approx
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


def test_basic_setup(behemoth_, wolf_, fighter_, blackmage_):

    behemoth, wolf, fighter, blackmage = behemoth_, wolf_, fighter_, blackmage_
    advs, monsters = [fighter, blackmage], [behemoth, wolf]
    
    battle = Battle(advs, monsters)
    names = [unit.name for unit in battle.turn_order]
    assert names == ["Behemoth", "Wolf", "Fighter", "BlackMage"]

    assert battle.next_turn().name == "Behemoth"

    assert len(battle.turn_order) == 3

    assert battle.next_turn().name == "Wolf"

    assert len(battle.turn_order) == 2

    battle.next_turn()

    battle.next_turn()

    assert len(battle.turn_order) == 0

    assert battle.round_count == 0

    assert (battle.next_turn().name == "Behemoth" or battle.next_turn().name == "Wolf")

    assert len(battle.turn_order) == 3

    assert battle.round_count == 1


def test_tick_cd(behemoth_, wolf_, fighter_, blackmage_):

    behemoth, wolf, fighter, blackmage = behemoth_, wolf_, fighter_, blackmage_
    advs, monsters = [fighter, blackmage], [behemoth, wolf]
    
    battle = Battle(advs, monsters)
    trample = Trample()
    behemoth.learn_skill(trample)
    with patch("random.random", side_effect=[0, 0]):
        behemoth.use(trample, battle.adventurers)
    assert trample.remaining_cooldown == trample._cooldown
    print(fighter._all_known_skills)
    battle.tick_cooldowns()
    assert trample.remaining_cooldown == trample._cooldown - 1
