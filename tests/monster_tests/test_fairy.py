import pytest
from monsters.magical.fairy import Fairy
from adventurers.adventurer import Adventurer
from jobs.warrior_classes.fighter import Fighter
from monsters.magical.fairy_skills import StarStream, FaeBlessing, ForestWind, MischievousMirage
from combat.compute_stat_buff import compute_increase_amount
from monsters.beasts.wolf import Wolf
from pytest import approx
from unittest.mock import patch

@pytest.fixture(autouse=True)
def patch_random_uniform():
    with patch("random.uniform", return_value=1.0):
        yield 

@pytest.fixture
def fairy_():
    f = Fairy(
        level=50,
        deterministic=True
    )
    return f

@pytest.fixture
def fighter_factory():
    def create_f():
        f = Fighter()
        return Adventurer(name="", job=f, level=55, deterministic=True)
    return create_f

@pytest.fixture
def wolf_factory():
    def create_w():
        w = Wolf(level=50, deterministic=True)
        return w
    return create_w


def test_forest_wind(fairy_, wolf_factory):
    fairy = fairy_
    wolf = wolf_factory()
    wolf.update_hp(-277)
    assert wolf.hp == 200
    fw = ForestWind()
    fairy.learn_skill(fw)
    INIT_MP = fairy.mp
    fairy.use(fw, wolf)
    assert wolf.hp == approx(208 + 1.05 * (0.30 * fairy.wisdom + 0.1 * fairy.charisma + 0.03 * fairy.luck))
    assert fairy.mp == approx(INIT_MP - (8 + 1.65 * fairy.level ** 0.60))


def test_m_mirage(fairy_):
    mm = MischievousMirage()
    fairy = fairy_
    INIT_MP = fairy.mp
    INIT_AGI = fairy.agility
    INIT_SPD = fairy.speed
    INIT_LCK = fairy.luck
    fairy.learn_skill(mm)
    agi_buff = compute_increase_amount(fairy, fairy, "agility", [0.75])
    spd_buff = compute_increase_amount(fairy, fairy, "speed", [0.75])
    fairy.use(mm, fairy)
    assert fairy.mp == approx(INIT_MP - (12 + 1.75 * 50 ** 0.6))
    assert fairy.speed == approx(INIT_SPD + spd_buff)
# Too lazy to actually compute the values, but printing them says they are fine


def test_star_stream(fairy_, fighter_factory):
    fighter = fighter_factory()
    fairy = fairy_
    ss = StarStream()
    fairy.learn_skill(ss)
    INIT_MP = fairy.mp
    INIT_HP = fighter.hp
    with patch("random.random", side_effect=[0,0]):
        fairy.use(ss, fighter)
    assert fairy.mp == approx(INIT_MP - (10 + 2.0 * 50 ** 0.6))
    assert fighter.hp == approx(INIT_HP - 1.15 * (fairy.matk/ 2 - fighter.mdef / 4))


def test_fae_blessing(fairy_, wolf_factory):
    fairy = fairy_
    print(fairy.hp)
    wolves = [wolf_factory() for _ in range(3)]
    for wolf in wolves:
        wolf.hp = 200
    INIT_AGI = wolves[0].agility
    print(INIT_AGI)
    fb = FaeBlessing()
    agi_buff = compute_increase_amount(fairy, wolves[0], "agility", [0.5])
    fairy.learn_skill(fb)
    fairy.use(fb, wolves)
    heal_amt = 8 + 0.5 * 1.05 * (0.30 * fairy.wisdom + 0.10 * fairy.charisma + 0.03 * fairy.luck)
    for i in range(len(wolves)):
        print(agi_buff)
        print(wolves[i].agility)
        assert wolves[i].hp == approx(200 + heal_amt)
        assert wolves[i].agility == approx(INIT_AGI + agi_buff)
