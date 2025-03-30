class BehaviorNode:
    def execute(self, unit, battle, data):
        """Base node for behavior tree"""
        pass


class Sequence(BehaviorNode):
    """Executes child nodes in order until one fails."""
    def __init__(self, children):
        self.children = children
        
    def execute(self, unit, battle, data):
        for child in self.children:
            result = child.execute(unit, battle, data)
            if not result:
                return False
        return True


class Selector(BehaviorNode):
    """Executes child nodes in priority order, until one succeeds."""
    def __init__(self, children):
        self.children = children
        
    def execute(self, unit, battle, data):
        for child in self.children:
            result = child.execute(unit, battle, data)
            if result:
                return True
        return False
