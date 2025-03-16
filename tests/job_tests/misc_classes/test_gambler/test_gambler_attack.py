import pytest
from pytest import approx
from operator import add
from adventurers.adventurer import Adventurer
from jobs.misc_classes.gambler import Gambler
from jobs.warrior_classes.fighter import Fighter
from unittest.mock import patch


@pytest.fixture
def gambler_():
    c = Gambler()
    a = Adventurer(
        name="",
        job=c,
        level=10,
        deterministic=True
    )
    return a

@pytest.fixture
def fighter_():
    c = Fighter()
    a = Adventurer(
        name="",
        job=c,
        level=10,
        deterministic=True
    )
    return a

def test_init(gambler_):
    gambler = gambler_
    assert len(gambler.job.hand) == 0
    assert gambler.luck == 110
    gambler.job.add_card("spade", 8)
    assert len(gambler.job.hand) == 1
    for i in range(4):
        gambler.job.add_card("spade", i)
    gambler.job.add_card("heart", 0)
    assert len(gambler.job.hand) == 5

def test_attack(gambler_, fighter_):
    gambler = gambler_
    fighter = fighter_
    INIT_HP = fighter.job.growth_rates["hp"] * (fighter.level + 3)
    DMG_1 = 19.00438095238
    DMG_2 = 28.506571428571426
    assert fighter.hp == INIT_HP
    # No crit:
    with patch("random.random", side_effect=[0, 1]), \
               patch("random.uniform", return_value=1.00):
        gambler.attack(fighter)
    
    assert fighter.hp == approx(INIT_HP - DMG_1)
    assert len(gambler.job.hand) == 1
    assert gambler.job.hand[0] == ('spade', 9)
    # Crit:
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        gambler.attack(fighter)
    assert fighter.hp == approx(INIT_HP - DMG_1 - DMG_2)
    assert len(gambler.job.hand) == 2
    assert gambler.job.hand[1] == ('spade', 8)
