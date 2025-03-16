import pytest
from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.mage_classes.spellblade import SpellBlade
from jobs.warrior_classes.fighter import Fighter
from monsters.beasts.behemoth import Behemoth
from monsters.beasts.wolf import Wolf
from combat.skills.mage_classes.spellblade import Fusion, ElementalHarmony
from core.stats.attributes import Attributes
from unittest.mock import patch

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
def b_():
    b = Behemoth(
        level=10,
        deterministic=True
    )
    return b

@pytest.fixture
def w_():
    w = Wolf(
        level=10,
        deterministic=True
    )
    return w


def test_fusion(sb_, b_, w_):
    sb = sb_
    b = b_
    w = w_
    fusion = Fusion()
    sb.learn_skill(fusion)
    B_INIT_HP = b.growth_rates["hp"] * 13
    W_INIT_HP = w.growth_rates["hp"] * 13
    DMG_1 = 1.15 * (0.6 * (sb.watk + sb.matk) / 2 - b.mdef / 4) * 1.10 * 0.75
    DMG_2 = 1.15 * (0.6 * (sb.watk + sb.matk) / 2 - w.mdef / 4) * 1.10
    assert b.hp == B_INIT_HP
    assert w.hp == W_INIT_HP
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        sb.use(fusion, b)
        fusion.remaining_cooldown = 0
    assert b.hp == approx(B_INIT_HP - DMG_1)

    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        sb.use(fusion, w)
    assert w.hp == approx(W_INIT_HP - DMG_2)

def test_eh(sb_):
    sb = sb_
    eh = ElementalHarmony()

    INIT_STR = sb.job.growth_rates["strength"] * 10
    INIT_INT = sb.job.growth_rates["intellect"] * 10
    INIT_MP = sb.job.growth_rates["mp"] * 13
    assert sb.strength == INIT_STR and sb.intellect == INIT_INT and sb.mp == INIT_MP

    sb.learn_skill(eh)

    sb.use(eh, sb)

    STR_GAIN = INIT_INT * .25
    INT_GAIN = INIT_STR * .25
    assert sb.strength == INIT_STR + STR_GAIN
    assert sb.intellect == INIT_INT + INT_GAIN
