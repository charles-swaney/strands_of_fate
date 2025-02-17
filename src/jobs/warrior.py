from base import Job


class Warrior(Job):
    @property
    def base_growth_rates(self):
        return {
            "hp": 8,
            "mp": 2,
            "strength": 7,
            "toughness": 7,
            "dexterity": 5,
            "agility": 4,
            "intellect": 2,
            "willpower": 3,
            "tenacity": 6,
            "charisma": 3,
            "luck": 4
        }

    def on_level_up(self, adventurer):
        adventurer.hp += self.base_growth_rates["hp"]
        adventurer.mp += self.base_growth_rates["mp"]
        adventurer.strength += self.base_growth_rates["strength"]
