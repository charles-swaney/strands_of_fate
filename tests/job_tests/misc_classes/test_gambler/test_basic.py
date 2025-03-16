# Gambler's basic abilities consist of those that "do something" along with drawing a card.
# Their advanced abilities are those that rely on the cards in their deck for special effects.
import pytest
import random
from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.misc_classes.gambler import Gambler
from monsters.beasts.wolf import Wolf
from unittest.mock import patch
from combat.skills.misc_classes.gambler import TrickUpTheSleeve


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
    assert wolf.hp == INIT_HP

    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        gambler.use(trick, wolf)
        trick.remaining_cooldown = 0

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
