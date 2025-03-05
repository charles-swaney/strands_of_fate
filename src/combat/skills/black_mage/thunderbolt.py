from actions.spell import Spell


class Thunderbolt(Spell):
    def __init__(self):
        super().__init__(
            name="Thunderbolt",
            cost_type="mp",
            base_cost=12,
            cost_scaling=1.25,
            cooldown=3,
            magnitude=1.25,
            element="lightning",
            spell_type="damage"
        )
        self.target_type="multiple"
