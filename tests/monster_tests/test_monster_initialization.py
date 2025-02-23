from monsters.beasts.wolf import Wolf


def test_monster_initialization():
    wolf = Wolf(
        monster_species="wolf",
        level=1,
        aptitude=10,
        deterministic=True
    )
    assert wolf.hp == 11.0
    assert wolf.get_total_stat("strength") == 9
    assert wolf.class_aptitude == 0
    assert wolf.aptitude == 10
    assert wolf.get_element_res("fire") == wolf.get_element_res("water")
    assert wolf.get_element_res("lightning") == 1.0
    assert wolf.get_weapon_res("slash") == 1.25

    beefy = Wolf(
        monster_species="wolf",
        level=1,
        aptitude=5,
        deterministic=True,
        hp=1000
    )
    assert beefy.hp == 1000


def test_monster_levelup():
    wolf = Wolf(
        monster_species="wolf",
        deterministic=True
    )
    assert wolf.level == 1
    for _ in range(50):
        wolf.level_up()
    assert wolf.level == 51
    assert wolf.aptitude == 5
    for _ in range(25):
        wolf.level_up()
    assert wolf.level == 76
