from adventurers.adventurer import Adventurer
from jobs.mage_classes.hemomancer import Hemomancer
from combat.skills.mage_classes.hemomancer.transfusion import Transfusion
from monsters.beasts.boar import Boar
from pytest import approx
from unittest.mock import patch


def test_learn_cast():
    h = Hemomancer()
    t = Transfusion()

    hemom = Adventurer(
        name="",
        job=h,
        level=1,
        deterministic=True
    )

    boar = Boar(
        level=1,
        deterministic=True
    )

    assert len(hemom.skills["Hemomancer"]) == 0
    hemom.learn_skill(t)
    assert len(hemom.skills["Hemomancer"]) == 1

    THEORETICAL_DMG = 1.15 * (hemom.matk / 2 - boar.mdef / 4) * 0.80

    assert boar.hp == 40
    assert hemom.hp == 40
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
            hemom.use(t, boar)

    assert (40 - boar.hp == approx(THEORETICAL_DMG))
    # Subtract cost, add 0.40% healing rate
    assert hemom.hp == 40 - 6 + 0.4 * THEORETICAL_DMG
    t.remaining_cooldown = 0
    # Test missing
    with patch("random.random", side_effect=[1]), \
               patch("random.uniform", return_value=1.00):

            hemom.use(t, boar)
    assert (40 - boar.hp == approx(THEORETICAL_DMG))
    assert hemom.hp == 40 - 6 + 0.4 * THEORETICAL_DMG - 6


def test_transfusion():
    h = Hemomancer()
    t = Transfusion()

    hemom = Adventurer(
        name="",
        job=h,
        level=80,
        deterministic=True
    )

    boar = Boar(
        level=55,
        deterministic=True
    )
    start_hp = hemom.hp
    boar_start = boar.hp
    hemom.learn_skill(t)
    # MISS
    with patch("random.random", side_effect=[1]), \
               patch("random.uniform", return_value=1.00):

        hemom.use(t, boar)
    t.remaining_cooldown = 0
    assert hemom.hp == approx(start_hp - (4 + 2 * 80 ** 0.6))
    with patch("random.random", side_effect=[0]), \
            patch("random.uniform", return_value=1.00):

        hemom.use(t, boar)
        t.remaining_cooldown = 0
    THEORETICAL_DMG = 1.15 * (hemom.matk / 2 - boar.mdef / 4) * 0.80
    
    assert (boar_start - boar.hp == approx(THEORETICAL_DMG))
    assert hemom.hp == 830

    hemom.update_hp(-829)
    assert hemom.hp == 1

    assert hemom.can_access(t) == True
    assert t.can_be_used(hemom) == False

    hemom.update_hp(55)

    assert hemom.can_access(t) == True
    assert t.can_be_used(hemom) == True

    with patch("random.random", side_effect=[0]), \
            patch("random.uniform", return_value=1.00):

        hemom.use(t, boar)
    assert hemom.hp == approx(151.3814062)
