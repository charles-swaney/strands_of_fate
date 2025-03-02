from adventurers.adventurer import Adventurer
from combat.spells.shared.fire import Fire
from jobs.mage_classes.black_mage import BlackMage
from monsters.beasts.behemoth import Behemoth
import random


def test_learn_spells():
    b = BlackMage()

    blackmage = Adventurer(
        name="",
        job=b,
        level=1,
        deterministic=True
    )
    assert blackmage.spells == []
    assert blackmage
    fire_spell = Fire()
    blackmage.learn_spell(fire_spell)
    assert fire_spell in blackmage.spells