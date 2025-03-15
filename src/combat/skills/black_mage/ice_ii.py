from actions.skill import Skill


class Ice_II(Skill):
    def __init__(self):
        """
        Describe the Ice_II skill.
        """
        super().__init__(
            name="Ice",
            cost_type="mp",
            base_cost=6,
            cost_scaling=1.5,
            cooldown=3,
            magnitude=1.10,
            element="Ice",
            skill_type="damage"
        )
        self.target_type="multiple"
