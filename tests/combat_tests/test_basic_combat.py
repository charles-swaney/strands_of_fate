from adventurers.adventurer import Adventurer
from jobs.warrior_classes.fighter import Fighter
from jobs.warrior_classes.guardian import Guardian
from jobs.thief_classes.archer import Archer
from monsters.beasts.direwolf import DireWolf
from combat.damage_calculator import compute_damage_physical
import random
from equipment.armor import Armor
from equipment.weapon import Weapon


def test_simple_combat():
    random.seed(1301)
    direwolf = DireWolf(level=10, deterministic=True)
    f = Fighter()
    a = Archer()

    fighter = Adventurer(
        name="",
        job=f,
        level=10,
        deterministic=True
    )
    archer = Adventurer(
        name="",
        job=a,
        level=10,
        deterministic=True
    )
    assert direwolf.hp == 120
    fighter.attack(direwolf)
    assert direwolf.hp < 93
    archer.attack(direwolf)
    assert direwolf.hp < 75
    direwolf.attack(fighter)
    assert fighter.hp < 35
    direwolf.attack(fighter)
    assert fighter.hp <= 0

def test_equipment_combat():
    random.seed(1301)
    direwolf = DireWolf(level=25, deterministic=True)
    a = Archer()
    g = Guardian()

    archer = Adventurer(
        name="",
        job=a,
        level=25,
        deterministic=True,
    )

    guardian = Adventurer(
        name="",
        job=g,
        level=50,
        deterministic=True
    )

    bow = Weapon(
        name="",
        slot="weapon",
        item_type="bow",
        damage_type="ranged",
        watk=17
    )

    assert direwolf.hp == 300
    archer.attack(direwolf)
    assert direwolf.hp < 265
    archer.equip("weapon", bow)
    archer.attack(direwolf)

    assert direwolf.hp < 210
    assert guardian.hp == 400
    direwolf.attack(guardian)
    assert guardian.hp < 380

    armor = Armor(
        name="",
        slot="armor",
        item_type="heavy_armor",
        wdef=50,
        mdef=5
    )
    guardian.equip("armor", armor)
    assert guardian.hp < 376
    assert guardian.hp > 375
    direwolf.attack(guardian)
    assert guardian.hp > 363
    guardian.unequip("armor")
    direwolf.attack(guardian)
    assert guardian.hp < 341
    assert guardian.hp > 339


def test_bonus_equipment_combat():
    random.seed(1332)
    g = Guardian()

    guardian = Adventurer(
        name="",
        job=g,
        level=65,
        deterministic=True
    )
    f = Fighter()

    fighter = Adventurer(
        name="",
        job=f,
        level=65,
        deterministic=True
    )

    reg_sword = Weapon(
        name="",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=50,
        wdef=10)

    bonus_sword = Weapon(
        name="",
        slot="weapon",
        item_type="sword",
        damage_type="slash",
        watk=50,
        wdef=10,
        equipment_stat_bonuses={
            "strength": 25,
            "toughness": 30
        }
    )
    old_hp = 520
    assert guardian.hp == 520
    fighter.attack(guardian)
    new_hp_1 = guardian.hp
    print(guardian.hp)
    dmg_no_equip = old_hp - new_hp_1
    print(f"theoretical dmg without equip: ")
    print(compute_damage_physical(
        fighter,
        guardian,
        "standard",
        "blunt"
    ))
    print(f"damage without equipment: {dmg_no_equip}")
    fighter.equip("weapon", reg_sword)
    print(f"theoretical dmg  reg sword: ")
    print(compute_damage_physical(
        fighter,
        guardian,
        "standard",
        "slash"
    ))
    fighter.attack(guardian)
    new_hp_2 = guardian.hp
    dmg_reg_sword = new_hp_1 - new_hp_2
    print(f"damage with reg sword: {dmg_reg_sword}")
    print(guardian.hp)

    fighter.equip("weapon", bonus_sword)
    print(f"theoretical dmg bonus sword: ")
    print(compute_damage_physical(
        fighter,
        guardian,
        "standard",
        "slash"
    ))
    fighter.attack(guardian)
    new_hp_3 = guardian.hp
    dmg_bonus_sword = new_hp_2 - new_hp_3
    print(f"damage with bonus sword: {dmg_bonus_sword}")
    assert dmg_bonus_sword > dmg_reg_sword
    assert dmg_reg_sword > dmg_no_equip
    print(guardian.hp)
