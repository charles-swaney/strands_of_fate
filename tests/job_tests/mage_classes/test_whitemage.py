import pytest
from pytest import approx
from unittest.mock import patch
from adventurers.adventurer import Adventurer
from jobs.mage_classes.white_mage import WhiteMage
from jobs.warrior_classes.fighter import Fighter
from combat.skills.shared.heal import Heal


@pytest.fixture
def whitemage_():
    c = WhiteMage()
    a = Adventurer(
        name="",
        job=c,
        level=5,
        deterministic=True
    )
    return a

@pytest.fixture
def fighter_():
    c = Fighter()
    a = Adventurer(
        name="",
        job=c,
        level=5,
        deterministic=True
    )
    return a


def test_heal(whitemage_, fighter_):
    heal = Heal()
    wm = whitemage_
    f = fighter_
    assert wm.hp == 32
    assert wm.mp == 48
    f.update_hp(-53)
    wm.learn_skill(heal)
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        wm.use(heal, f)
        heal.remaining_cooldown = 0
    THEORETICAL_HEAL = 24.0125
    assert f.hp == approx(3 + THEORETICAL_HEAL)
    assert wm.mp == approx(48 - (6.626527804403767))

    for _ in range(55):
        wm.level_up()
        f.level_up()
    f.update_hp(2000)
    wm.update_mp(2000)
    assert f.hp == 441
    assert wm.mp == 378
    f.update_hp(-3)
    assert f.hp == 438
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        wm.use(heal, f)
        heal.remaining_cooldown = 0
    assert f.hp == 441
    assert wm.mp == approx(378 - 15.66516134976123)
    f.update_hp(-400)
    assert f.hp == 41
    THEORETICAL_HEAL = 200.15
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        wm.use(heal, f)
        heal.remaining_cooldown = 0
    assert f.hp == approx(41 + THEORETICAL_HEAL)
