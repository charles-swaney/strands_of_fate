from actions.skill import Skill


class Fire(Skill):
    def __init__(self):
        super().__init__(
            name="Fire",
            cost_type="mp",
            base_cost=4,
            cost_scaling=1.0,
            cooldown=2,
            magnitude=1.0,
            element="fire",
            skill_type="damage"
        )
        self.target_type="single"
