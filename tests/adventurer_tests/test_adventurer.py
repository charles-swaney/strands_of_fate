from adventurers.adventurer import Adventurer
from jobs.misc_classes.bard import Bard
from jobs.misc_classes.gambler import Gambler


def test_adventurer_initialization():
    """
    Tests:
    - stat initialization
    - stat override
    - effect of aptitude on stat growth
    - adventurers initialized with no equipment
    - equipment bonuses properly intialized as None
    """
    bard_job = Bard()
    adventurer_1 = Adventurer(
        name="William",
        job=bard_job,
        deterministic=True
    )
    adventurer_2 = Adventurer(
        name="Sarah",
        job=bard_job,
        aptitude=10,
        deterministic=True,
        hp=17,
    )
    assert adventurer_1.base_stats.get_stat("hp") == 20
    assert adventurer_1.aptitude == 5
    assert adventurer_1.base_stats.get_stat("luck") == 8
    assert adventurer_2.base_stats.get_stat("hp") == 17
    assert adventurer_2.aptitude == 10
    assert (adventurer_2.base_stats.get_stat("charisma") ==
            adventurer_1.base_stats.get_stat("charisma"))
    for item in adventurer_1.equipment.items().values():
        assert item is None
    for bonus in adventurer_1.equipment_bonuses.items():
        assert bonus is None


def test_level_up():
    """
    Tests:
    - level growth properly increases stats and preserves aptitude
    - higher aptitude -> better growths
    - class change works properly
    - levels_gained counts properly across multiple classes
    """
    bard_job = Bard()
    adventurer_1 = Adventurer(
        name="William",
        job=bard_job,
        deterministic=True
    )
    adventurer_2 = Adventurer(
        name="Sarah",
        job=bard_job,
        aptitude=10,
        hp=17,
        deterministic=True
    )
    for _ in range(49):
        adventurer_1.level_up()
        adventurer_2.level_up()
    adventurer_2.job = Gambler()
    assert adventurer_1.level == 50
    for _ in range(25):
        adventurer_1.level_up()
        adventurer_2.level_up()
    assert adventurer_1.level == 75
    assert adventurer_1.aptitude == 5
    assert adventurer_1.base_stats.get_stat("hp") == 390
    assert adventurer_1.levels_gained["Bard"] == 74
    assert adventurer_2.base_stats.get_stat("hp") == 362
    assert adventurer_2.levels_gained["Bard"] == 49
    assert adventurer_2.levels_gained["Gambler"] == 25
