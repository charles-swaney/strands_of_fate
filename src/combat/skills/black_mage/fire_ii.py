from actions.skill import Skill


class Fire(Skill):
    def __init__(self):
        super().__init__(
            name="Fire",
            cost_type="mp",
            base_cost=6,
            cost_scaling=1.5,
            cooldown=3,
            magnitude=1.10,
            element="fire",
            skill_type="damage"
        )
        self.target_type="multiple"
