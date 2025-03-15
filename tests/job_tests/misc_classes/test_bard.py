import pytest
from pytest import approx
from unittest.mock import patch
from adventurers.adventurer import Adventurer
from jobs.misc_classes.bard import Bard
from jobs.warrior_classes.fighter import Fighter
from combat.skills.bard.torching_tempo import TorchingTempo
from core.stats.attributes import Attributes


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

def test_tt(bard_, fighter_):
    tt = TorchingTempo()
    b = bard_
    f = fighter_
    assert b.hp == 40
    START_MP = 56

    START_STR, START_DEX = 45, 25
    STR_INCREASE_1 = 21.31
    DEX_INCREASE_1 = 19.95
    b.use(tt, f)
    tt.remaining_cooldown = 0
    assert f.total_stats.get_stat("strength") == START_STR + STR_INCREASE_1
    assert f.total_stats.get_stat("dexterity") == START_DEX + DEX_INCREASE_1
    f.stat_buffs = Attributes({})
    assert f.total_stats.get_stat("strength") == START_STR
    for _ in range(94):
        b.level_up()
        f.level_up()
    NEW_STR, NEW_DEX = 891, 495
    assert f.total_stats.get_stat("strength") == NEW_STR
    assert f.total_stats.get_stat("dexterity") == NEW_DEX
    STR_INCREASE_2 = 629.4524
    DEX_INCREASE_2 = 468.518
    b.use(tt, f)
    assert f.total_stats.get_stat("strength") == NEW_STR + STR_INCREASE_2
    assert f.total_stats.get_stat("dexterity") == NEW_DEX + DEX_INCREASE_2