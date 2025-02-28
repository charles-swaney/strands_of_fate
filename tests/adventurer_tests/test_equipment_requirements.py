import pytest
from adventurers.adventurer import Adventurer
from jobs.mage_classes.hemomancer import Hemomancer
from jobs.misc_classes.gambler import Gambler
from equipment.armor import Armor
from equipment.weapon import Weapon


def test_invalid_for_slot():
    hemomancer_class = Hemomancer()
    adventurer = Adventurer(
        name="joe",
        job=hemomancer_class
    )
    robe = Armor(
        name="robe",
        slot="armor",
        item_type="robe",
        wdef=2,
        mdef=20
    )
    robe_helm = Armor(
        name="robe_helm",
        slot="helmet",
        item_type="robe",
        wdef=3,
        mdef=10
    )
    robe_gauntlet = Armor(
        name="robe_gauntlet",
        slot="gauntlet",
        item_type="robe",
        wdef=5,
        mdef=5
    )
    dagger = Weapon(
        name="dagger",
        slot="weapon",
        item_type="dagger",
        damage_type="stab",
        watk=5
    )
    with pytest.raises(ValueError):
        adventurer.equip("helmet", robe)

    with pytest.raises(ValueError):
        adventurer.equip("robe", dagger)

    with pytest.raises(ValueError):
        adventurer.equip("gauntlet", robe_helm)

    with pytest.raises(ValueError):
        adventurer.equip("weapon", robe_gauntlet)

    for item in adventurer.equipment.items().values():
        assert item is None
    for bonus in adventurer.equipment_bonuses.items():
        assert bonus is None


def test_invalid_item_type():
    gambler_class = Gambler()
    adventurer = Adventurer(
        name="gambly joe",
        job=gambler_class
    )
    robe = Armor(
        name="robe",
        slot="armor",
        item_type="robe",
        wdef=2,
        mdef=20
    )
    robe_helm = Armor(
        name="robe_helm",
        slot="helmet",
        item_type="robe",
        wdef=3,
        mdef=10
    )
    robe_gauntlet = Armor(
        name="robe_gauntlet",
        slot="gauntlet",
        item_type="robe",
        wdef=5,
        mdef=5
    )
    hammer = Weapon(
        name="dagger",
        slot="weapon",
        item_type="hammer",
        damage_type="blunt",
        watk=5
    )
    with pytest.raises(ValueError):
        adventurer.equip("armor", robe)

    with pytest.raises(ValueError):
        adventurer.equip("weapon", hammer)

    with pytest.raises(ValueError):
        adventurer.equip("helmet", robe_helm)

    with pytest.raises(ValueError):
        adventurer.equip("gauntlet", robe_gauntlet)

    for item in adventurer.equipment.items().values():
        assert item is None
    for bonus in adventurer.equipment_bonuses.items():
        assert bonus is None


def test_both_invalid():
    gambler_class = Gambler()
    adventurer = Adventurer(
        name="gambly joe",
        job=gambler_class
    )
    robe = Armor(
        name="robe",
        slot="armor",
        item_type="robe",
        wdef=2,
        mdef=20
    )
    with pytest.raises(ValueError):
        adventurer.equip("weapon", robe)


def test_valid_equips():
    hemomancer_class = Hemomancer()
    adventurer = Adventurer(name="joe", job=hemomancer_class)

    robe = Armor(name="robe", slot="armor", item_type="robe", wdef=2, mdef=20)
    dagger = Weapon(name="dagger", slot="weapon", item_type="dagger", damage_type="stab", watk=5)

    adventurer.equip("armor", robe)
    adventurer.equip("weapon", dagger)

    assert adventurer.equipment.get_item("armor") == robe
    assert adventurer.equipment.get_item("weapon") == dagger
