from monsters.beasts.behemoth import Behemoth
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.guardian import Guardian
from monsters.beasts.behemoth_skills.trample import Trample
from pytest import approx
from unittest.mock import patch


def test_attack():
    b = Behemoth(
        level=50,
        deterministic=True
    )
    g = Guardian()
    guardian = Adventurer(
        name="",
        job=g,
        level=80,
        deterministic=True
    )
    init_hp = guardian.hp
    print(guardian.hp)
    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        b.attack(guardian)
        after_attack_hp = guardian.hp
    THEORETICAL_DMG = 94.1573333
    assert init_hp - after_attack_hp == approx(THEORETICAL_DMG)
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.attack(guardian)
        after_crit_hp = guardian.hp
    assert after_attack_hp - after_crit_hp == approx(THEORETICAL_DMG * 1.50)


def test_learn_skills():
    b = Behemoth(
        level=50,
        deterministic=True
    )
    g = Guardian()
    g1 = Adventurer(
        name="",
        job=g,
        level=55,
        deterministic=True
    )
    trample = Trample()
    assert not b.can_access(trample)
    assert len(b.skills) == 0
    b.learn_skill(trample)
    assert len(b.skills) == 1
    b.learn_skill(trample)
    assert len(b.skills) == 1

    assert b.can_access(trample)

    assert trample.can_be_used(b)
    b.update_hp(-741)
    assert b.hp == 1
    assert not trample.can_be_used(b)
    b.update_hp(741)
    assert b.hp == 742
    b.update_mp(-211)
    assert b.mp == 1
    assert not trample.can_be_used(b)

def test_trample_multiple():
    b = Behemoth(
        level=50,
        deterministic=True
    )

    trample = Trample()
    b.learn_skill(trample)

    g = Guardian()
    g1 = Adventurer(
        name="",
        job=g,
        level=55,
        deterministic=True
    )

    g2 = Adventurer(
        name="",
        job=g,
        level=55,
        deterministic=True
    )

    g3 = Adventurer(
        name="",
        job=g,
        level=55,
        deterministic=True
    )

    g4 = Adventurer(
        name="",
        job=g,
        level=55,
        deterministic=True
    )
    assert b.level == 50
    assert g4.level == 55
    init_b_hp = 14 * (50 + 3)
    init_b_mp = 4 * (50 + 3)
    assert b.hp == init_b_hp
    assert b.mp == init_b_mp
    # Trample has a random uniform roll for damage noise and a
    # random.random roll for hitting or not, for each target.
    advs = [g1, g2, g3, g4]
    for adv in advs:
        print(adv.hp)
    with patch("random.random", side_effect=[0, 0, 0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, advs)
        trample.remaining_cooldown = 0
    THEORETICAL_DAMAGE = 117.878
    THEORETICAL_COST = 28.91279105182546
    assert b.hp == approx(init_b_hp - THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - THEORETICAL_COST)
    for adv in advs:
        assert adv.hp == approx(464 - THEORETICAL_DAMAGE)
    with patch("random.random", side_effect=[0, 0, 0, 0]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, [g1, g3])
        trample.remaining_cooldown = 0
    assert b.hp == approx(init_b_hp - 2 * THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - 2 * THEORETICAL_COST)
    assert g1.hp == approx(464 - 2 * THEORETICAL_DAMAGE)
    assert g3.hp == approx(464 - 2 * THEORETICAL_DAMAGE)

    with patch("random.random", side_effect=[1]), \
               patch("random.uniform", return_value=1.00):
        b.use(trample, [g1])
        trample.remaining_cooldown = 0
    assert b.hp == approx(init_b_hp - 3 * THEORETICAL_COST)
    assert b.mp == approx(init_b_mp - 3 * THEORETICAL_COST)
    assert g1.hp == approx(464 - 2 * THEORETICAL_DAMAGE)
