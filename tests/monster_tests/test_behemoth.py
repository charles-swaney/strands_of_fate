import pytest
from monsters.beasts.behemoth import Behemoth
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.guardian import Guardian
from monsters.beasts.behemoth_skills import Trample, IronHide, ExposeWeakness, EarthenGrasp, UnyieldingWill
from pytest import approx
from unittest.mock import patch
BASE_HP = 689
BASE_MP = 212


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


def test_expose_weakness(behemoth_, guardian_factory):
    behemoth = behemoth_
    guardian = guardian_factory()
    init_hp = guardian.hp
    init_tgh = guardian.toughness
    init_ten = guardian.tenacity
    expose_weakness = ExposeWeakness()
    THEORETICAL_DMG_1 = 0.5 * (behemoth.watk / 1.75 - guardian.wdef / 3.75) * 0.85
    behemoth.learn_skill(expose_weakness)
    assert behemoth.mp == BASE_MP
    COST = 8 + 2.0 * behemoth.level ** 0.60

    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        behemoth.use(expose_weakness, guardian)
        expose_weakness.remaining_cooldown = 0
    hp1 = guardian.hp
    assert behemoth.mp == approx(BASE_MP - COST)
    dmg_1 = init_hp - hp1
    assert dmg_1 == approx(THEORETICAL_DMG_1)
    assert guardian.toughness == init_tgh * 0.60
    assert guardian.tenacity == init_ten * 0.60
    THEORETICAL_DMG_2 = 69.58342857142856
    # Debuff roll misses
    with patch("random.random", side_effect=[0, 1, 0]), \
               patch("random.uniform", return_value=1.00):
        behemoth.use(expose_weakness, guardian)
        expose_weakness.remaining_cooldown = 0
    hp2 = guardian.hp
    assert hp1 - hp2 == approx(THEORETICAL_DMG_2)
    assert guardian.toughness == init_tgh * 0.60
    with patch("random.random", side_effect=[0, 0, 0]), \
               patch("random.uniform", return_value=1.00):
        behemoth.use(expose_weakness, guardian)
        expose_weakness.remaining_cooldown = 0
    assert hp2 - guardian.hp == approx(THEORETICAL_DMG_2)
    assert guardian.toughness == init_tgh * 0.36


def test_earthen_grasp(behemoth_, guardian_factory):
    behemoth = behemoth_
    guardian = guardian_factory()
    init_hp = guardian.hp
    init_agi = guardian.agility
    init_dex = guardian.dexterity
    earthen_grasp = EarthenGrasp()
    THEORETICAL_DMG_1 = 0.75 * (behemoth.watk / 2 - guardian.mdef / 4) * 1.15
    behemoth.learn_skill(earthen_grasp)
    assert behemoth.mp == BASE_MP
    COST = 10 + 2.0 * behemoth.level ** 0.60
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        behemoth.use(earthen_grasp, guardian)
        earthen_grasp.remaining_cooldown = 0
    assert behemoth.mp == approx(BASE_MP - COST)
    assert guardian.hp == approx(init_hp - THEORETICAL_DMG_1)
    assert guardian.agility == approx(init_agi * 2/3)
    assert guardian.dexterity == approx(init_dex * 2/3)


def test_unyielding_will(behemoth_):
    b = behemoth_
    BASE_STR = b.strength
    BASE_INT = b.intellect
    COST = 12 + 1.75 * 50 ** 0.6
    uw = UnyieldingWill()
    b.learn_skill(uw)
    assert len(b.skills) == 1
    b.use(uw, b)
    uw.remaining_cooldown = 0
    assert b.mp == BASE_MP - COST
    assert b.strength == approx(BASE_STR * 0.75)
    assert b.intellect == approx(BASE_INT * 0.75)
    b.update_hp(-600)
    assert b.hp == 89
    with patch("random.uniform", return_value=1.00):
        b.use(uw, b)
    assert b.mp == approx(BASE_MP - 2 * COST)
    HEAL = 0.75 * 1.05 * 0.43 * b.tenacity * (1 + (1 - 89/689) / 2)
    NEW_HP = 89 + HEAL
    assert b.hp == approx(NEW_HP)
