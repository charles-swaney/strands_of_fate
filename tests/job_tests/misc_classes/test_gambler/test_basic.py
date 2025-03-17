# Gambler's basic abilities consist of those that "do something" along with drawing a card.
# Their advanced abilities are those that rely on the cards in their deck for special effects.
import pytest
import random
from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.misc_classes.gambler import Gambler
from jobs.warrior_classes.fighter import Fighter
from monsters.beasts.wolf import Wolf
from unittest.mock import patch
from combat.skills.misc_classes.gambler import TrickUpTheSleeve, LuckyCharm


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
def wolf_():
    w = Wolf(
        level=10,
        deterministic=True
    )
    return w

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

def test_trick(gambler_, wolf_):
    trick = TrickUpTheSleeve()
    gambler = gambler_
    assert len(gambler.skills["Gambler"]) == 0
    gambler.learn_skill(trick)
    assert len(gambler.skills["Gambler"]) == 1
    wolf = wolf_
    COST = 6 + 1.5 * 10 ** 0.6
    wdef = wolf.wdef
    watk = gambler.watk
    DMG = 0.85 * (watk / 1.75 - wdef / 3.75) * 0.9
    INIT_HP = wolf.growth_rates["hp"] * (wolf.level + 3)
    INIT_MP = gambler.job.growth_rates["mp"] * (gambler.level + 3)
    assert wolf.hp == INIT_HP

    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        gambler.use(trick, wolf)
        trick.remaining_cooldown = 0
    assert gambler.mp == INIT_MP - COST
    assert wolf.hp == INIT_HP - DMG
    assert gambler.job.hand[0] == ('spade', 8)
    assert len(gambler.job.hand) == 2

    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        gambler.use(trick, wolf)
        trick.remaining_cooldown = 0
    assert len(gambler.job.hand) == 4
    
    with patch("random.random", side_effect=[0, 1]), \
               patch("random.uniform", return_value=1.00):
        gambler.attack(wolf)
    assert len(gambler.job.hand) == 5

    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        gambler.use(trick, wolf)
        trick.remaining_cooldown = 0
    assert len(gambler.job.hand) == 5


def test_charm(gambler_, fighter_):
    lcharm = LuckyCharm()
    gambler = gambler_
    fighter = fighter_
    assert len(gambler.skills["Gambler"]) == 0
    gambler.learn_skill(lcharm)
    assert len(gambler.skills["Gambler"]) == 1
    COST = 8 + 2.0 * 10 ** 0.6
    HEAL = 5 + 1.05 * 0.43 * gambler_.job.growth_rates["luck"] * (gambler.level) * 0.30
    INIT_HP = fighter.job.growth_rates["hp"] * (fighter.level + 3)
    INIT_MP = gambler.job.growth_rates["mp"] * (gambler.level + 3)
    assert fighter.hp == INIT_HP
    fighter.update_hp(-(INIT_HP - 1))
    assert fighter.hp == 1
    assert gambler.mp == INIT_MP
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        gambler.use(lcharm, fighter)
    assert fighter.hp == approx(1 + HEAL)
    assert gambler.mp == approx(INIT_MP - COST)

    assert len(gambler.job.hand) == 2
    assert gambler.job.hand[0] == ('heart', 9)
