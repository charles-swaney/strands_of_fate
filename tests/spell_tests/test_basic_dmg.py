from unittest.mock import patch
from pytest import approx
from adventurers.adventurer import Adventurer
from combat.spells.shared.fire import Fire
from combat.spells.shared.earth import Earth
from combat.spells.shared.light import Light
from jobs.mage_classes.black_mage import BlackMage
from monsters.beasts.behemoth import Behemoth


def test_spell_damage():
    # NOTE: spells only involve two rolls: one for hit chance, one for random damage perturbation
    # ALSO NOTE: black mages can't learn fire, earth, etc. this is just to test
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=99,
        deterministic=True
    )
    behemoth = Behemoth(
        level=99,
        deterministic=True
    )
    
    THEORETICAL_FIRE_DMG = 1.15 * (blackmage.matk / 2 - behemoth.mdef / 4) * 1.0 * 0.75
    THEORETICAL_EARTH_DMG = 1.15 * (blackmage.matk / 2 - behemoth.mdef / 4) * 1.0 * 0.50
    THEORETICAL_LIGHT_DMG = 1.15 * (blackmage.matk / 2 - behemoth.mdef / 4) * 1.0 * 1.00

    fire_spell = Fire()
    earth_spell = Earth()
    light_spell = Light()
    blackmage.learn_skill(fire_spell)
    blackmage.learn_skill(earth_spell)
    blackmage.learn_skill(light_spell)

    start_hp = behemoth.hp
    with patch("random.random", side_effect=[0]), \
               patch("random.uniform", return_value=1.00):
        blackmage.use(fire_spell, behemoth)

    after_fire_hp = behemoth.hp
    fire_dmg = start_hp - after_fire_hp
    assert fire_dmg == approx(THEORETICAL_FIRE_DMG)

    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        blackmage.use(earth_spell, behemoth)
    after_earth_hp = behemoth.hp
    earth_dmg = after_fire_hp - after_earth_hp
    assert earth_dmg == approx(THEORETICAL_EARTH_DMG)

    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        blackmage.use(light_spell, behemoth)
    after_light_hp = behemoth.hp
    light_dmg = after_earth_hp - after_light_hp
    assert light_dmg == approx(THEORETICAL_LIGHT_DMG)


def test_spell_miss():
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=99,
        deterministic=True
    )
    behemoth = Behemoth(
        level=99,
        deterministic=True
    )
    
    THEORETICAL_FIRE_DMG = 0

    fire_spell = Fire()
    blackmage.learn_skill(fire_spell)

    start_hp = behemoth.hp
    with patch("random.random", side_effect=[1.00]), \
               patch("random.uniform", return_value=1.00):
        blackmage.use(fire_spell, behemoth)

    after_fire_hp = behemoth.hp
    fire_dmg = start_hp - after_fire_hp
    assert fire_dmg == approx(THEORETICAL_FIRE_DMG)
    assert blackmage.mp < 7 * 99