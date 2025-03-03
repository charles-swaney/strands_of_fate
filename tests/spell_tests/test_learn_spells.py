from adventurers.adventurer import Adventurer
from combat.skills.shared.fire import Fire
from combat.skills.shared.ice import Ice
from combat.skills.shared.lightning import Lightning
from jobs.mage_classes.black_mage import BlackMage
from monsters.beasts.behemoth import Behemoth
from pytest import approx


def test_learn_spells():
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=25,
        deterministic=True
    )
    assert len(blackmage.skills["BlackMage"]) == 0
    fire_spell = Fire()
    blackmage.learn_skill(fire_spell)
    assert fire_spell in blackmage.skills["BlackMage"]
    assert fire_spell in blackmage.skillset.primary_skillset
    assert blackmage.can_access(fire_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 1


def test_learn_repeated():
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=25,
        deterministic=True
    )
    assert len(blackmage.skills["BlackMage"]) == 0
    fire_spell = Fire()
    assert blackmage.can_access(fire_spell) == False
    blackmage.learn_skill(fire_spell)
    assert fire_spell in blackmage.skills["BlackMage"]
    assert fire_spell in blackmage.skillset.primary_skillset
    assert blackmage.can_access(fire_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 1
    blackmage.learn_skill(fire_spell)
    blackmage.learn_skill(fire_spell)
    assert blackmage.can_access(fire_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 1


def test_learn_multiple():
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=25,
        deterministic=True
    )
    assert len(blackmage.skills["BlackMage"]) == 0
    fire_spell = Fire()
    ice_spell = Ice()
    lightning_spell = Lightning()
    blackmage.learn_skill(fire_spell)
    assert fire_spell in blackmage.skillset.primary_skillset
    assert blackmage.can_access(fire_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 1

    blackmage.learn_skill(ice_spell)
    assert ice_spell in blackmage.skillset.primary_skillset
    assert blackmage.can_access(ice_spell) == True
    assert blackmage.can_access(fire_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 2

    blackmage.learn_skill(lightning_spell)
    assert lightning_spell in blackmage.skillset.primary_skillset
    assert blackmage.can_access(ice_spell) == True
    assert blackmage.can_access(fire_spell) == True
    assert blackmage.can_access(lightning_spell) == True
    assert len(blackmage.skills["BlackMage"]) == 3

def test_spell_costs():
    LVL_1_COST = 5
    LVL_25_COST = 10.8986483073
    LVL_99_COST = 19.753647253

    behemoth = Behemoth(
        lvl=99
    )

    b = BlackMage()
    fire_spell = Fire()
    blackmage = Adventurer(
        name="",
        job=b,
        level=1,
        deterministic=True
    )
    blackmage.learn_skill(fire_spell)
    assert fire_spell.cost(blackmage) == LVL_1_COST
    blackmage.use(fire_spell, behemoth)
    assert blackmage.mp == 23
    assert blackmage.hp == 16

    blackmage2 = Adventurer(
        name="",
        job=b,
        level=25,
        deterministic=True
    )
    blackmage2.learn_skill(fire_spell)
    assert blackmage2.mp == 7 * 28
    assert fire_spell.cost(blackmage2) == approx(LVL_25_COST)
    fire_spell.tick_cooldown()
    fire_spell.tick_cooldown()
    blackmage2.use(fire_spell, behemoth)
    assert blackmage2.mp == approx(7 * 28 - LVL_25_COST)

    blackmage3 = Adventurer(
        name="",
        job=b,
        level=99,
        deterministic=True
    )

    blackmage3.learn_skill(fire_spell)
    assert blackmage3.mp == 7 * 102
    assert fire_spell.cost(blackmage3) == approx(LVL_99_COST)
    fire_spell.tick_cooldown()
    fire_spell.tick_cooldown()
    blackmage3.use(fire_spell, behemoth)
    assert blackmage3.mp == approx(7 * 102 - LVL_99_COST)


def test_mana_costs():
    b = BlackMage()
    behemoth = Behemoth(
        lvl=99
    )
    fire_spell = Fire()
    blackmage = Adventurer(
        name="",
        job=b,
        level=1,
        deterministic=True
    )
    blackmage.learn_skill(fire_spell)
    assert fire_spell.can_be_used(blackmage) == True
    for _ in range(4):
        blackmage.use(fire_spell, behemoth)
        fire_spell.tick_cooldown()
        fire_spell.tick_cooldown()
        assert fire_spell.can_be_used(blackmage) == True
    blackmage.use(fire_spell, behemoth)
    fire_spell.tick_cooldown()
    fire_spell.tick_cooldown()
    assert fire_spell.can_be_used(blackmage) == False

def test_cooldowns():
    b = BlackMage()
    behemoth = Behemoth(
        lvl=99
    )
    fire_spell = Fire()
    blackmage = Adventurer(
        name="",
        job=b,
        level=99,
        deterministic=True
    )
    blackmage.learn_skill(fire_spell)
    assert fire_spell.can_be_used(blackmage) == True
    blackmage.use(fire_spell, behemoth)
    fire_spell.tick_cooldown()
    assert fire_spell.can_be_used(blackmage) == False
    fire_spell.tick_cooldown()
    assert fire_spell.can_be_used(blackmage) == True
