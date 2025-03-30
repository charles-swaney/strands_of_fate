from ai.behavior_nodes.behavior_node import BehaviorNode


# TODO This is a bit more complicated since it probably needs to do some checks for unit hp, etc.

class UseMultiTargetHealSkill(BehaviorNode):
    """
    Attempt to use a skill that heals multiple targets.
    """
    raise NotImplementedError


class UseHealSkill(BehaviorNode):
    """
    Attempt to use a skill that buffs a single target.

    Note: this should typically occur after a check for `UseMultiTargetBuffSkill`,
        as if there are multiple allies remaining, most Monsters should prioritize
        buffing multiple. So this is usually executed only if there is only one ally
        remaining. Despite this, the unit should use multi-target buff skills if available.
    """
    raise NotImplementedError
