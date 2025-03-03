from actions.spell import Spell


class Light(Spell):
    def __init__(self):
        super().__init__(
            name="Light",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown = 2,
            magnitude=1.0,
            element = "light",
            spell_type="damage"
        )
        self.target_type = "single"
