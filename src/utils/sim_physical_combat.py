from typing import Union
from adventurers.adventurer import Adventurer
from monsters.monster import Monster


def sim_physical_combat(unit1: Union[Adventurer, Monster],
                        unit2: Union[Adventurer, Monster]):
    """
    Have unit1 and unit2 attack each other until one of them dies.
    """
    marker1 = unit1.job.job_name if isinstance(unit1, Adventurer) else unit1.species_name
    marker2 = unit2.job.job_name if isinstance(unit2, Adventurer) else unit2.species_name
    count = 0
    while unit1.hp > 0 and unit2.hp > 0 and count < 25:
        if unit1.total_stats.get_stat("speed") > unit2.total_stats.get_stat("speed"):
            old_hp_2 = unit2.hp
            unit1.attack(unit2)
            damage_to_unit2 = old_hp_2 - unit2.hp
            print(f"{marker1} deals {damage_to_unit2} damage to {marker2}")
            print(f"{marker2} has {unit2.hp} hp remaining")
            
            if unit2.hp > 0:
                old_hp_1 = unit1.hp
                unit2.attack(unit1)
                damage_to_unit1 = old_hp_1 - unit1.hp
                print(f"{marker2} deals {damage_to_unit1} damage to {marker1}")
                print(f"{marker1} has {unit1.hp} hp remaining")
            count += 1
        else:
            old_hp_1 = unit1.hp
            unit2.attack(unit1)
            damage_to_unit1 = old_hp_1 - unit1.hp
            print(f"{marker2} deals {damage_to_unit1} damage to {marker1}")
            print(f"{marker1} has {unit1.hp} hp remaining")
            
            if unit1.hp > 0:
                old_hp_2 = unit2.hp
                unit1.attack(unit2)
                damage_to_unit2 = old_hp_2 - unit2.hp
                print(f"{marker1} deals {damage_to_unit2} damage to {marker2}")
                print(f"{marker2} has {unit2.hp} hp remaining")
            count += 1

    if unit1.hp > 0:
        print(f"{marker1} survives with {unit1.hp} hp")
    else:
        print(f"{marker2} survives with {unit2.hp} hp")
