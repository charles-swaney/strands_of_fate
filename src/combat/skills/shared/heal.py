from actions.skill import Skill


class Fire(Skill):
    def __init__(self):
        super().__init__(
            name="Heal",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=1.0,
            element=None,
            skill_type="heal"
        )
        self.target_type="single"
