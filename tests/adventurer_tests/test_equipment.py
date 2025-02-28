from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.fighter import Fighter
from equipment.armor import Armor
from equipment.weapon import Weapon

THEORETICAL_BASE_WATK = 9.18
THEORETICAL_BASE_WDEF = 5.18
THEORETICAL_BASE_MDEF = 3.93


def test_equip_unequip_item():
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Joe",
        job=fighter_job,
        deterministic=True
    )
    longsword = Weapon(
        name="longsword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=17,
        wdef=2
    )
    broadsword = Weapon(
        name="Broadsword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=25
    )
    assert adventurer.watk == THEORETICAL_BASE_WATK
    adventurer.equip("weapon", longsword)
    assert adventurer.watk == THEORETICAL_BASE_WATK + longsword.watk
    adventurer.equip("weapon", broadsword)
    assert adventurer.watk == THEORETICAL_BASE_WATK + broadsword.watk
    adventurer.unequip("weapon")
    assert adventurer.watk == THEORETICAL_BASE_WATK


def test_simple_equipment_bonuses():
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job,
        deterministic=True
    )
    bonus_longsword = Weapon(
        name="bonus_longsword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=17,
        wdef=2,
        equipment_stat_bonuses={
            "strength": 10,
            "toughness": 5
        }
    )
    old_base_stats = adventurer.base_stats
    old_total_stats = adventurer.total_stats
    assert adventurer.watk == THEORETICAL_BASE_WATK
    assert adventurer.wdef == THEORETICAL_BASE_WDEF
    adventurer.equip("weapon", bonus_longsword)
    assert adventurer.base_stats.stats == old_base_stats.stats
    assert adventurer.total_stats.stats != old_total_stats.stats
    assert adventurer.get_total_stat("strength") == \
        (adventurer.get_base_stat("strength") + 10)
    assert adventurer.get_total_stat("toughness") == \
        (adventurer.get_base_stat("toughness") + 5)
    assert adventurer.watk == THEORETICAL_BASE_WATK + 27
    assert adventurer.wdef == THEORETICAL_BASE_WDEF + 7
    adventurer.unequip("weapon")
    assert adventurer.watk == THEORETICAL_BASE_WATK
    assert adventurer.wdef == THEORETICAL_BASE_WDEF


def test_complex_equipment_bonuses():
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job,
        deterministic=True
    )
    complex_sword = Weapon(
        name="complex_sword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=10,
        wdef=5,
        equipment_stat_bonuses={
            "strength": 10,
            "toughness": 5,
            "intellect": 5,
            "tenacity": 10,
            "luck": 10
        }
    )
    old_base_stats = adventurer.base_stats
    assert adventurer.mdef == THEORETICAL_BASE_MDEF
    assert adventurer.watk == THEORETICAL_BASE_WATK
    adventurer.equip("weapon", complex_sword)
    assert adventurer.get_total_stat("luck") == (adventurer.get_base_stat("luck") + 10)
    assert adventurer.base_stats.stats == old_base_stats.stats
    assert adventurer.watk == THEORETICAL_BASE_WATK + 10 + 10 + 0.3
    assert adventurer.mdef == approx(THEORETICAL_BASE_MDEF + 1.5 + 0.3)


def test_multiple_simple_equipments():
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job,
        deterministic=True
    )
    helmet = Armor(
        name="helmet",
        slot="helmet",
        item_type="light_armor",
        wdef=5,
        mdef=5
    )
    armor = Armor(
        name="armor",
        slot="armor",
        item_type="light_armor",
        wdef=10,
        mdef=5
    )
    gauntlets = Armor(
        name="gauntlets",
        slot="gauntlet",
        item_type="light_armor",
        wdef=5,
        mdef=0,
        watk=5
    )
    sword = Weapon(
        name="sword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=10
    )
    assert (adventurer.mdef == THEORETICAL_BASE_MDEF and
            adventurer.watk == THEORETICAL_BASE_WATK and
            adventurer.wdef == THEORETICAL_BASE_WDEF)

    adventurer.equip("helmet", helmet)
    adventurer.equip("armor", armor)
    adventurer.equip("gauntlet", gauntlets)
    adventurer.equip("weapon", sword)

    assert (adventurer.mdef == THEORETICAL_BASE_MDEF + 5 + 5 + 0 and
            adventurer.watk == THEORETICAL_BASE_WATK + 5 + 10 and
            adventurer.wdef == THEORETICAL_BASE_WDEF + 5 + 10 + 5)

    adventurer.unequip("helmet")
    adventurer.unequip("armor")
    adventurer.unequip("gauntlet")
    adventurer.unequip("weapon")

    assert (adventurer.mdef == THEORETICAL_BASE_MDEF and
            adventurer.watk == THEORETICAL_BASE_WATK and
            adventurer.wdef == THEORETICAL_BASE_WDEF)


def test_multiple_complex_equipments():
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job,
        deterministic=True
    )
    helmet = Armor(
        name="helmet",
        slot="helmet",
        item_type="light_armor",
        wdef=5,
        mdef=5,
        equipment_stat_bonuses={
            "strength": 10,
            "toughness": 5
        }
    )
    armor = Armor(
        name="armor",
        slot="armor",
        item_type="light_armor",
        wdef=10,
        mdef=5,
        equipment_stat_bonuses={
            "toughness": 20,
            "wisdom": 10,
            "tenacity": 2,
            "luck": 5
        }
    )
    gauntlets = Armor(
        name="gauntlets",
        slot="gauntlet",
        item_type="light_armor",
        wdef=5,
        mdef=0,
        watk=5,
        equipment_stat_bonuses={
            "strength": 10,
            "tenacity": 10,
            "luck": 5
        }
    )
    sword = Weapon(
        name="sword",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=10,
        equipment_stat_bonuses={
            "strength": 2.2,
            "toughness": -5,
            "wisdom": 5,
            "tenacity": 10,
            "luck": 20
        }
    )
    assert (adventurer.mdef == THEORETICAL_BASE_MDEF and
            adventurer.watk == THEORETICAL_BASE_WATK and
            adventurer.wdef == THEORETICAL_BASE_WDEF)

    adventurer.equip("helmet", helmet)
    adventurer.equip("armor", armor)
    adventurer.equip("gauntlet", gauntlets)
    adventurer.equip("weapon", sword)

    assert adventurer.mdef == approx(THEORETICAL_BASE_MDEF + 5 + 5 + 0 +
                                (10 + 0.3 + 0.15 + 1.5 + 0.15 + 5 + 1.5 + 0.6))
    assert adventurer.watk == approx(THEORETICAL_BASE_WATK + 5 + 10 +
                                    (10 + 0.15 + 10 + 0.15 + 2.2 + 0.6))
    assert adventurer.wdef == approx(THEORETICAL_BASE_WDEF + 5 + 10 + 5 +
                                    (5 + 20 + 0.15 + 0.15 - 5 + 0.6))

    adventurer.unequip("helmet")
    adventurer.unequip("armor")
    adventurer.unequip("gauntlet")
    adventurer.unequip("weapon")

    assert (adventurer.mdef == THEORETICAL_BASE_MDEF and
            adventurer.watk == THEORETICAL_BASE_WATK and
            adventurer.wdef == THEORETICAL_BASE_WDEF)
