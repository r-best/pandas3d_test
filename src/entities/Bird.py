from panda3d.core import CollisionBox, CollisionNode, CollisionHandlerFloor, CollisionRay

from .BaseEntity import BaseEntity

class Bird(BaseEntity):
    """
    """
    MODEL = "models/panda-model"

    def __init__(self):
        super().__init__()
        self.setScale(0.05)

    # Override
    def act(self, task):
        """Main logic loop, overridden from BaseEntity"""
        # self.nodePath.setH(self.nodePath.getH() + 0.5)
        return task.cont
