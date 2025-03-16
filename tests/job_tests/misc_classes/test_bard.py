import pytest
from pytest import approx
from operator import add
from adventurers.adventurer import Adventurer
from jobs.misc_classes.bard import Bard
from jobs.warrior_classes.fighter import Fighter
from jobs.mage_classes.spellblade import SpellBlade
from combat.skills.misc_classes.bard import TorchingTempo, FortifyingChant, SpunkyDitty
from core.stats.attributes import Attributes
START_MP = 56


@pytest.fixture
def bard_():
    c = Bard()
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

@pytest.fixture
def sb_():
    c = SpellBlade()
    a = Adventurer(
        name="",
        job=c,
        level=5,
        deterministic=True
    )
    return a


def test_tt(bard_, fighter_, sb_):
    tt = TorchingTempo()
    b = bard_
    f = fighter_
    sb = sb_
    assert b.hp == 40

    START_STR, START_DEX = 45, 25
    STR_INCREASE_1 = 24.7025
    DEX_INCREASE_1 = 23.6125
    b.use(tt, f)
    tt.remaining_cooldown = 0
    assert f.strength == START_STR + STR_INCREASE_1
    assert f.dexterity == START_DEX + DEX_INCREASE_1
    f.stat_buffs = Attributes({})
    assert f.strength == START_STR
    assert b.mp == approx(START_MP - 9.93979)
    for _ in range(94):
        b.level_up()
        f.level_up()
    NEW_STR, NEW_DEX = 891, 495
    assert f.strength == NEW_STR
    assert f.dexterity == NEW_DEX
    STR_INCREASE_2 = 470.4881
    DEX_INCREASE_2 = 415.4045
    b.use(tt, f)
    assert f.strength == NEW_STR + STR_INCREASE_2
    assert f.dexterity == NEW_DEX + DEX_INCREASE_2
    with pytest.raises(Exception) as e:
        b.use(tt, [f, sb])

def test_fc(bard_, fighter_):
    fc = FortifyingChant()
    b = bard_
    f = fighter_
    START_TGH= 25
    START_TEN = 25
    TGH_INCREASE_1 = 23.6125
    TEN_INCREASE_1 = 23.6125
    b.use(fc, f)
    fc.remaining_cooldown = 0
    assert f.toughness == START_TGH + TGH_INCREASE_1
    assert f.tenacity == START_TEN + TEN_INCREASE_1
    assert b.mp == approx(START_MP - 10.333770877266215)


def test_sd(bard_, fighter_, sb_):
    sd = SpunkyDitty()
    LVL_5_COST = 19.8795834132113
    LVL_99_COST = 59.26094175893539
    b = bard_
    INIT_MP = b.mp
    f = fighter_
    sb = sb_
    fighter_lvl_5_stats = [9 * 5, 2 * 5, 4 * 5, 6 * 5]
    sb_lvl_5_stats = [7 * 5, 7 * 5, 6 * 5, 6 * 5]
    assert [f.strength, f.intellect, f.agility, f.luck] == fighter_lvl_5_stats
    assert [sb.strength, sb.intellect, sb.agility, sb.luck] == sb_lvl_5_stats
    b.use(sd, [f, sb])
    sd.remaining_cooldown = 0
    assert b.mp == approx(INIT_MP - LVL_5_COST)
    assert [f.strength, f.intellect, f.agility, f.luck] == \
        approx(list(map(add, fighter_lvl_5_stats, [24.7025, 22.795, 23.34, 23.885])))
    assert [sb.strength, sb.intellect, sb.agility, sb.luck] == \
        approx(list(map(add, sb_lvl_5_stats, [24.1575, 24.1575, 23.885, 23.885])))
    
    for _ in range(94):
        b.level_up()
        f.level_up()
        sb.level_up()
    f_99_stats = [9 * 99, 2 * 99, 4 * 99, 6 * 99]
    sb_99_stats = [7 * 99, 7 * 99, 6 * 99, 6 * 99]
    f.stat_buffs = Attributes({})
    sb.stat_buffs = Attributes({})
    assert [f.strength, f.intellect, f.agility, f.luck] == f_99_stats
    assert [sb.strength, sb.intellect, sb.agility, sb.luck] == sb_99_stats
    b.mp += 1000
    b.use(sd, [f, sb])
    assert b.mp == approx(714 - LVL_99_COST)
    assert [f.strength, f.intellect, f.agility, f.luck] == \
        approx(list(map(add, f_99_stats, [470.4881, 374.0918, 401.6336, 429.1754])))
    assert [sb.strength, sb.intellect, sb.agility, sb.luck] == \
        approx(list(map(add, sb_99_stats, [442.9463, 442.9463, 429.1754, 429.1754])))
