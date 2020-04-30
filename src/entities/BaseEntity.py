from direct.actor.Actor import Actor

class BaseEntity(Actor):
    """
    """
    # Default entity model (overwritten by subclasses)
    MODEL = "models/teapot"

    def __init__(self):
        super().__init__(self.MODEL)
        self.tasks = list()
