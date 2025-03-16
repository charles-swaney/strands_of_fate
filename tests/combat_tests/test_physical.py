import pytest
from unittest.mock import patch
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.ronin import Ronin
from jobs.warrior_classes.guardian import Guardian
from monsters.beasts.direwolf import DireWolf
from monsters.beasts.behemoth import Behemoth
from src.utils.sim_physical_combat import sim_physical_combat
from equipment.weapon import Weapon
from equipment.armor import Armor


@pytest.fixture
def ronin_():
    c = Ronin()
    a = Adventurer(
        name="",
        job=c,
        level=50,
        deterministic=True
    )
    return a

@pytest.fixture
def guardian_():
    c = Guardian()
    a = Adventurer(
        name="",
        job=c,
        level=50,
        deterministic=True
    )
    return a

@pytest.fixture
def dw_():
    dw = DireWolf(
        level=50,
        deterministic=True
    )
    return dw

@pytest.fixture
def b_():
    b = Behemoth(
        level=50,
        deterministic=True
    )
    return b


def test_dmg(ronin_, dw_, b_, guardian_):
    ronin = ronin_
    dw = dw_
    b = b_
    g = guardian_

    sword = Weapon(
        name="",
        slot="weapon",
        item_type="katana",
        damage_type="slash",
        watk=90,
        wdef=30,
        equipment_stat_bonuses={
            "strength": 30,
            "dexterity": 15
        }
    )
    armor = Armor(
        name="",
        slot="armor",
        item_type="light_armor",
        wdef=55,
        mdef=10
    )
    helm = Armor(
        name="",
        slot="helmet",
        item_type="light_armor",
        wdef=30,
        mdef=5
    )

    sim_physical_combat(ronin, g)

    ronin.equip("weapon", sword)
    ronin.equip("armor", armor)
    ronin.equip("helmet", helm)
