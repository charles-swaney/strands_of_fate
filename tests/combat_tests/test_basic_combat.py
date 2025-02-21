from combat.damage_calculator import compute_damage_magical, compute_damage_physical
from adventurers.adventurer import Adventurer
from jobs.mage_classes.black_mage import BlackMage
from jobs.warrior_classes.guardian import Guardian
from monsters.beasts.direwolf import DireWolf
from equipment.armor import Armor
from equipment.weapon import Weapon
import random


def test_physical_dmg():
    # Checks that physical dmg works with different wdef and damage type vs monsters
    random.seed(1301)
    bm = BlackMage()
    gd = Guardian()

    blackmage = Adventurer(
        name="1",
        job=bm,
        level=10
    )

    guardian = Adventurer(
        name="2",
        job=gd,
        level=10
    )

    direwolf = DireWolf(
        level=10
    )
    dmg1 = compute_damage_physical(direwolf, blackmage, "standard", "slash")
    dmg2 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    dmg3 = compute_damage_physical(guardian, direwolf, "standard", "blunt")
    dmg4 = compute_damage_physical(guardian, direwolf, "standard", "ranged")
    assert dmg1 > dmg2
    assert dmg2 > dmg3
    assert dmg4 > dmg3


def test_physical_equipment():
    # check that equipping and unequipping equipment works with dmg including stat bonuses
    random.seed(1301)
    gd = Guardian()

    guardian = Adventurer(
        name="2",
        job=gd,
        level=10
    )

    direwolf = DireWolf(
        level=10
    )
    dmg1 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    armor = Armor(
        name="1",
        slot="armor",
        item_type="heavy_armor",
        wdef=20,
        mdef=10
    )
    guardian.equip("armor", armor)
    dmg2 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    guardian.unequip("armor")
    dmg3 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    assert dmg2 < dmg1
    assert dmg2 < dmg3
    guardian.equip("armor", armor)
    gauntlets = Armor(
        name="2",
        slot="gauntlet",
        item_type="heavy_armor",
        wdef=10,
        mdef=10
    )
    guardian.equip("gauntlet", gauntlets)
    dmg4 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    assert dmg4 < dmg2

    good_armor = Armor(
        name="2",
        slot="armor",
        item_type="heavy_armor",
        wdef=20,
        mdef=10,
        equipment_stat_bonuses={
            "toughness": 50
        }
    )
    guardian.equip("armor", good_armor)
    dmg5 = compute_damage_physical(direwolf, guardian, "standard", "slash")
    assert dmg5 < dmg4

    guard_dmg1 = compute_damage_physical(guardian, direwolf, "standard", "blunt")
    hammer = Weapon(
        name="3",
        slot="weapon",
        item_type="hammer",
        watk=25
    )
    guardian.equip("weapon", hammer)
    guard_dmg2 = compute_damage_physical(guardian, direwolf, "standard", "blunt")
    assert guard_dmg2 > guard_dmg1
    guardian.unequip("weapon")
    guard_dmg3 = compute_damage_physical(guardian, direwolf, "standard", "blunt")
    assert guard_dmg2 > guard_dmg3

    good_hammer = Weapon(
        name="3",
        slot="weapon",
        item_type="hammer",
        watk=25,
        equipment_stat_bonuses={
            "strength": 25
        }
    )
    guardian.equip("weapon", good_hammer)
    guard_dmg4 = compute_damage_physical(guardian, direwolf, "standard", "blunt")
    assert guard_dmg4 > guard_dmg2


def test_magical_dmg():
    # test that magical dmg works with elemental resistances, equipping and unequipping
    random.seed(1301)
    bm = BlackMage()

    blackmage = Adventurer(
        name="1",
        job=bm,
        level=10
    )

    direwolf = DireWolf(
        level=10
    )

    base_dmg_fire = compute_damage_magical(blackmage, direwolf, "fire")
    dmg_lightning = compute_damage_magical(blackmage, direwolf, "lightning")
    assert base_dmg_fire > dmg_lightning

    robes = Armor(
        name="1",
        slot="armor",
        item_type="robe",
        wdef=1,
        mdef=10,
        matk=10
    )
    blackmage.equip("armor", robes)
    robes_dmg_fire = compute_damage_magical(blackmage, direwolf, "fire")
    assert robes_dmg_fire > base_dmg_fire

    good_robes = Armor(
        name="1",
        slot="armor",
        item_type="robe",
        wdef=1,
        mdef=10,
        matk=10,
        equipment_stat_bonuses={
            "intellect": 100
        }
    )
    blackmage.equip("armor", good_robes)
    good_robes_dmg_fire = compute_damage_magical(blackmage, direwolf, "fire")
    assert good_robes_dmg_fire > robes_dmg_fire
    blackmage.unequip("armor")
    new_dmg_fire = compute_damage_magical(blackmage, direwolf, "fire")
    assert new_dmg_fire < robes_dmg_fire
