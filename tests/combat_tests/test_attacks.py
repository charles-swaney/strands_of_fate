from unittest.mock import patch
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.ronin import Ronin
from monsters.beasts.direwolf import DireWolf
from equipment.weapon import Weapon
from pytest import approx


def test_fixed_damage():
    r = Ronin()
    wolf = DireWolf(level=25, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=25,
        deterministic=True
    )
    init_hp = wolf.hp
    assert init_hp == 12 * 28
    EXPECTED_DAMAGE = 0.85 * (ronin.watk / 1.75 - wolf.wdef / 3.75)
    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        ronin.attack(wolf)
    dmg = init_hp - wolf.hp
    assert dmg == approx(EXPECTED_DAMAGE)


def test_crit_damage():
    r = Ronin()
    wolf = DireWolf(level=25, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=25,
        deterministic=True
    )
    init_hp = wolf.hp
    assert init_hp == 12 * 28
    EXPECTED_DAMAGE = 0.85 * (ronin.watk / 1.75 - wolf.wdef / 3.75) * 1.5
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.00):
        ronin.attack(wolf)
    dmg = init_hp - wolf.hp
    assert dmg == approx(EXPECTED_DAMAGE)


def test_miss_no_damage():
    r = Ronin()
    wolf = DireWolf(level=25, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=25,
        deterministic=True
    )
    init_hp = wolf.hp
    assert init_hp == 12 * 28
    EXPECTED_DAMAGE = 0
    with patch("random.random", side_effect=[1.00, 0]), \
               patch("random.uniform", return_value=1.00):
        ronin.attack(wolf)
    dmg = init_hp - wolf.hp
    assert dmg == approx(EXPECTED_DAMAGE)


def test_weapon_resistance_baseline():
    r = Ronin()
    wolf = DireWolf(level=25, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=25,
        deterministic=True
    )
    ranged = Weapon(
        name="",
        slot="weapon",
        item_type="katana",
        damage_type="ranged",
        watk = 35
    )
    ronin.equip("weapon", ranged)
    init_hp = wolf.hp
    assert init_hp == 12 * 28
    EXPECTED_DAMAGE = 0.85 * (ronin.watk / 1.75 - wolf.wdef / 3.75) * 1.25
    with patch("random.random", side_effect=[0, 1.00]), \
               patch("random.uniform", return_value=1.00):
        ronin.attack(wolf)
    dmg = init_hp - wolf.hp
    assert dmg == approx(EXPECTED_DAMAGE)


def test_multiple_interactions():
    r = Ronin()
    wolf = DireWolf(level=25, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=25,
        deterministic=True
    )
    ranged = Weapon(
        name="",
        slot="weapon",
        item_type="katana",
        damage_type="ranged",
        watk = 35
    )
    ronin.equip("weapon", ranged)
    init_hp = wolf.hp
    assert init_hp == 12 * 28
    EXPECTED_DAMAGE = 0.85 * (ronin.watk / 1.75 - wolf.wdef / 3.75) * 1.25 * 1.5 * 1.04
    with patch("random.random", side_effect=[0, 0]), \
               patch("random.uniform", return_value=1.04):
        ronin.attack(wolf)
    dmg = init_hp - wolf.hp
    assert dmg == approx(EXPECTED_DAMAGE)


def test_costs():
    r = Ronin()
    wolf = DireWolf(level=99, deterministic=True)

    ronin = Adventurer(
        name="",
        job=r,
        level=12,
        deterministic=True
    )
    START_HP = 12 * 102
    THEORETICAL_MP = 45
    THEORETICAL_HP = START_HP - 344
    assert ronin.mp == THEORETICAL_MP
    assert wolf.hp == START_HP

    for _ in range(344):
        with patch("random.random", side_effect=[0, 1.00]), \
            patch("random.uniform", return_value=1.00):
                ronin.attack(wolf)

    assert ronin.mp == THEORETICAL_MP
    assert ronin.hp == 6 * 15
    assert wolf.hp == THEORETICAL_HP