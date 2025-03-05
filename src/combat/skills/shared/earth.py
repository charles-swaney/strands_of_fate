from actions.spell import Spell


class Earth(Spell):
    def __init__(self):
        super().__init__(
            name="Earth",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=1.0,
            element="earth",
            spell_type="damage"
        )
        self.target_type="single"
