import random
from monsters.beasts.wolf import Wolf


def test_monster_initialization():
    random.seed(1301)
    wolf = Wolf(
        monster_species="wolf",
        level=1
    )
    assert wolf.hp == 12.0
    assert wolf.class_aptitude == 0
    assert wolf.get_element_res("fire") == wolf.get_element_res("water")
    assert wolf.get_element_res("lightning") == 1.0
    assert wolf.get_weapon_res("slash") == 1.25

def test_monster_levelup():
    random.seed(1301)
    wolf = Wolf(
        monster_species="wolf"
    )
    assert wolf.level == 1
    for _ in range(50):
        wolf.level_up()
    assert wolf.level == 51
    assert wolf.aptitude == 5
    for _ in range(25):
        wolf.level_up()
    assert wolf.level == 76