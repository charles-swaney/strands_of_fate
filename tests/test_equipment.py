import random
from pytest import approx
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.fighter import Fighter
from equipment.armor import Armor
from equipment.weapon import Weapon

THEORETICAL_BASE_WATK = 9.21
THEORETICAL_BASE_WDEF = 5.21
THEORETICAL_BASE_MDEF = 3.96


def test_equip_unequip_item():
    random.seed(1301)
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Joe",
        job=fighter_job
    )
    longsword = Weapon(
        name="longsword",
        weapon_type="sword",
        watk=17,
        wdef=2
    )
    broadsword = Weapon(
        name="Broadsword",
        weapon_type="sword",
        watk=25
    )
    assert adventurer.base_watk == THEORETICAL_BASE_WATK
    adventurer.equipment["weapon"] = longsword
    assert adventurer.base_watk == THEORETICAL_BASE_WATK + longsword.watk
    adventurer.equipment["weapon"] = broadsword
    assert adventurer.base_watk == THEORETICAL_BASE_WATK + broadsword.watk
    adventurer.equipment["weapon"] = None
    assert adventurer.base_watk == THEORETICAL_BASE_WATK

def test_simple_equipment_bonuses():
    random.seed(1301)
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job
    )
    bonus_longsword = Weapon(
        name="bonus_longsword",
        weapon_type="sword",
        watk=17,
        wdef=2,
        equipment_stat_bonuses={
            "strength": 10,
            "toughness": 5
        }
    )
    old_base_stats = adventurer.base_stats
    old_total_stats = adventurer.total_stats
    assert adventurer.base_watk == THEORETICAL_BASE_WATK
    assert adventurer.base_wdef == THEORETICAL_BASE_WDEF
    adventurer.equipment["weapon"] = bonus_longsword
    assert adventurer.base_stats.stats == old_base_stats.stats
    assert adventurer.total_stats.stats != old_total_stats.stats
    assert adventurer.total_stats.get_stat("strength") == (adventurer.base_stats.get_stat("strength") + 10)
    assert adventurer.total_stats.get_stat("toughness") == (adventurer.base_stats.get_stat("toughness") + 5)
    assert adventurer.base_watk == THEORETICAL_BASE_WATK + 27
    assert adventurer.base_wdef == THEORETICAL_BASE_WDEF + 7
    adventurer.equipment["weapon"] = None
    assert adventurer.base_watk == THEORETICAL_BASE_WATK
    assert adventurer.base_wdef == THEORETICAL_BASE_WDEF

def test_complex_equipment_bonuses():
    random.seed(1301)
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job
    )
    complex_sword = Weapon(
        name="complex_sword",
        weapon_type="sword",
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
    assert adventurer.base_mdef == THEORETICAL_BASE_MDEF
    assert adventurer.base_watk == THEORETICAL_BASE_WATK
    adventurer.equipment["weapon"] = complex_sword
    assert adventurer.total_stats.get_stat("luck") == (adventurer.base_stats.get_stat("luck") + 10)
    assert adventurer.base_stats.stats == old_base_stats.stats
    assert adventurer.base_watk == THEORETICAL_BASE_WATK + 10 + 10 + 0.3
    assert adventurer.base_mdef == THEORETICAL_BASE_MDEF + 1.5 + 0.3

def test_multiple_simple_equipments():
    random.seed(1301)
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job
    )
    helmet = Armor(
        name="helmet",
        armor_type="helmet",
        wdef=5,
        mdef=5
    )
    armor = Armor(
        name="armor",
        armor_type="armor",
        wdef=10,
        mdef=5
    )
    gauntlets = Armor(
        name="gauntlets",
        armor_type="gauntlets",
        wdef=5,
        mdef=0,
        watk=5
    )
    sword = Weapon(
        name="sword",
        weapon_type="sword",
        watk=10
    )
    assert (adventurer.base_mdef == THEORETICAL_BASE_MDEF and
            adventurer.base_watk == THEORETICAL_BASE_WATK and
            adventurer.base_wdef == THEORETICAL_BASE_WDEF)
    
    adventurer.equipment["helmet"] = helmet
    adventurer.equipment["armor"] = armor
    adventurer.equipment["gauntlets"] = gauntlets
    adventurer.equipment["sword"] = sword

    assert (adventurer.base_mdef == THEORETICAL_BASE_MDEF + 5 + 5 + 0 and
            adventurer.base_watk == THEORETICAL_BASE_WATK + 5 + 10 and
            adventurer.base_wdef == THEORETICAL_BASE_WDEF + 5 + 10 + 5)
    
    adventurer.equipment["helmet"] = None
    adventurer.equipment["armor"] = None
    adventurer.equipment["gauntlets"] = None
    adventurer.equipment["sword"] = None

    assert (adventurer.base_mdef == THEORETICAL_BASE_MDEF and
            adventurer.base_watk == THEORETICAL_BASE_WATK and
            adventurer.base_wdef == THEORETICAL_BASE_WDEF)

def test_multiple_complex_equipments():
    random.seed(1301)
    fighter_job = Fighter()
    adventurer = Adventurer(
        name="Charlotte",
        job=fighter_job
    )
    helmet = Armor(
        name="helmet",
        armor_type="helmet",
        wdef=5,
        mdef=5,
        equipment_stat_bonuses={
            "strength": 10,
            "toughness": 5
        }
    )
    armor = Armor(
        name="armor",
        armor_type="armor",
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
        armor_type="gauntlets",
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
        weapon_type="sword",
        watk=10,
        equipment_stat_bonuses={
            "strength": 2.2,
            "toughness": -5,
            "wisdom": 5,
            "tenacity": 10,
            "luck": 20
        }
    )
    assert (adventurer.base_mdef == THEORETICAL_BASE_MDEF and
            adventurer.base_watk == THEORETICAL_BASE_WATK and
            adventurer.base_wdef == THEORETICAL_BASE_WDEF)
    
    adventurer.equipment["helmet"] = helmet
    adventurer.equipment["armor"] = armor
    adventurer.equipment["gauntlets"] = gauntlets
    adventurer.equipment["sword"] = sword

    assert adventurer.base_mdef == approx(THEORETICAL_BASE_MDEF + 5 + 5 + 0 + (10 + 0.3 + 0.15 + 1.5 + 0.15 + 5 + 1.5 + 0.6))
    assert adventurer.base_watk == approx(THEORETICAL_BASE_WATK + 5 + 10 + (10 + 0.15 + 10 + 0.15 + 2.2 + 0.6))
    assert adventurer.base_wdef == approx(THEORETICAL_BASE_WDEF + 5 + 10 + 5 + (5 + 20 + 0.15 + 0.15 - 5 + 0.6))
    
    adventurer.equipment["helmet"] = None
    adventurer.equipment["armor"] = None
    adventurer.equipment["gauntlets"] = None
    adventurer.equipment["sword"] = None

    assert (adventurer.base_mdef == THEORETICAL_BASE_MDEF and
            adventurer.base_watk == THEORETICAL_BASE_WATK and
            adventurer.base_wdef == THEORETICAL_BASE_WDEF)


