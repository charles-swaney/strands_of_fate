import pytest
from monsters.beasts.behemoth import Behemoth
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.guardian import Guardian
from monsters.beasts.behemoth_skills.trample import Trample
from monsters.beasts.behemoth_skills.iron_hide import IronHide
import monsters.beasts.behemoth_skills as bsk
from pytest import approx
from unittest.mock import patch


@pytest.fixture
def behemoth_():
    b = Behemoth(
        level=50,
        deterministic=True
    )
    return b

@pytest.fixture
def guardian_factory():
    def create_guardian():
        g = Guardian()
        return Adventurer(name="", job=g, level=55, deterministic=True)
    return create_guardian

def test_attack(behemoth_, guardian_factory):
    b = behemoth_
    guardian = guardian_factory()
    init_hp = guardian.hp
    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        b.attack(guardian)
        after_attack_hp = guardian.hp
    THEORETICAL_DMG = 84.31352
    assert init_hp - after_attack_hp == approx(THEORETICAL_DMG)
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.attack(guardian)
        after_crit_hp = guardian.hp
    assert after_attack_hp - after_crit_hp == approx(THEORETICAL_DMG * 1.50)


def test_learn_skills(behemoth_):
    b = behemoth_
    trample = Trample()
    assert not b.can_access(trample)
    assert len(b.skills) == 0
    b.learn_skill(trample)
    assert len(b.skills) == 1
    b.learn_skill(trample)
    assert len(b.skills) == 1

    assert b.can_access(trample)

    assert trample.can_be_used(b)
    b.update_hp(-688)
    assert b.hp == 1
    assert not trample.can_be_used(b)
    b.update_hp(700)
    assert b.hp == 689
    b.update_mp(-211)
    assert b.mp == 1
    assert not trample.can_be_used(b)

def test_trample(behemoth_, guardian_factory):
    b = behemoth_
    advs = [guardian_factory() for _ in range(4)]

    trample = Trample()
    b.learn_skill(trample)

    assert b.level == 50
    init_b_hp = 13 * (50 + 3)
    init_b_mp = 4 * (50 + 3)
    assert b.hp == init_b_hp
    assert b.mp == init_b_mp
    # Trample has a random uniform roll for damage noise and a
    # random.random roll for hitting or not, for each target.
    with patch("random.random", side_effect=[0, 0, 0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, advs)
        trample.remaining_cooldown = 0
    THEORETICAL_DAMAGE = 84.3135238095238 * 0.75
    THEORETICAL_COST = 28.91279105182546
    assert b.hp == approx(init_b_hp - THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - THEORETICAL_COST)
    for adv in advs:
        assert adv.hp == approx(464 - THEORETICAL_DAMAGE)
    with patch("random.random", side_effect=[0, 0, 0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, [advs[1], advs[3]])
        trample.remaining_cooldown = 0
    assert b.hp == approx(init_b_hp - 2 * THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - 2 * THEORETICAL_COST)
    assert advs[1].hp == approx(464 - 2 * THEORETICAL_DAMAGE)
    assert advs[3].hp == approx(464 - 2 * THEORETICAL_DAMAGE)

    with patch("random.random", side_effect=[1]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, advs[1])
        trample.remaining_cooldown = 0
    assert b.hp == approx(init_b_hp - 3 * THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - 3 * THEORETICAL_COST)
    assert advs[1].hp == approx(464 - 2 * THEORETICAL_DAMAGE)


def test_ironhide(behemoth_, guardian_factory):
    b = behemoth_
    g = guardian_factory()
    for _ in range(44):
        g.level_up()
    BASE_HP = 689
    BASE_MP = 212
    BASE_TGH = 500
    BASE_TEN = 650
    COST = 12 + 1.75 * 50 ** 0.6
    assert (b.toughness == BASE_TGH and
            b.tenacity == BASE_TEN)
    BASE_DMG = 53.8964761905
    with patch("random.random", side_effect=[0, 1]), \
               patch("random.uniform", return_value=1.00):
        g.attack(b) 
    assert b.hp == approx(BASE_HP - BASE_DMG)
    ih = IronHide()
    b.learn_skill(ih)
    assert len(b.skills) == 1
    b.use(ih, b)
    assert b.mp == BASE_MP - COST
    assert b.hp == approx(BASE_HP - BASE_DMG - COST)
    OLD = b.hp
    assert (b.toughness == BASE_TGH + 0.25 * BASE_TEN and
            b.tenacity == BASE_TEN + 0.25 * BASE_TGH)
    with patch("random.random", side_effect=[0, 1]), \
               patch("random.uniform", return_value=1.00):
        g.attack(b)
        NEW_DMG = OLD - b.hp
    assert b.hp == approx(OLD - NEW_DMG)
