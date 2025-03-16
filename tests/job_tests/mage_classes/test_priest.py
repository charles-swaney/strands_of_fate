import pytest
from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.mage_classes.priest import Priest
from jobs.warrior_classes.fighter import Fighter
from jobs.mage_classes.spellblade import SpellBlade
from combat.skills.priest import EmboldeningChant
from core.stats.attributes import Attributes
from unittest.mock import patch

START_MP = 91

@pytest.fixture
def priest_():
    c = Priest()
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

@pytest.fixture
def sb_():
    c = SpellBlade()
    a = Adventurer(
        name="",
        job=c,
        level=10,
        deterministic=True
    )
    return a

def test_ec(priest_, fighter_, sb_):
    p = priest_
    f = fighter_
    sb = sb_
    ec = EmboldeningChant()
    p.learn_skill(ec)
    assert f.hp == 7 * 13
    with pytest.raises(Exception):
        p.use(ec, [f, sb])
    f.update_hp(-70)
    assert f.hp == 21
    assert f.toughness == 50

    assert p.mp == START_MP
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        p.use(ec, f)
    HEAL = 46.06875
    BONUS_TGH = 31.8
    assert f.hp == approx(21 + HEAL)
    assert f.toughness == approx(50 + BONUS_TGH)