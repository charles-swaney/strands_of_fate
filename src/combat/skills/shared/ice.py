from actions.spell import Spell


class Ice(Spell):
    def __init__(self):
        super().__init__(
            name="Ice",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=1.0,
            element="ice",
            spell_type="damage"
        )
        self.target_type="single"
