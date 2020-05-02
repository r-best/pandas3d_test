import random

from panda3d.core import CollisionBox, CollisionNode, CollisionHandlerFloor, CollisionRay

from .BaseEntity import BaseEntity

class Bird(BaseEntity):
    """
    """
    MODEL = "models/panda-model"

    speed = 1
    rotation = 3

    def __init__(self):
        super().__init__()
        self.actor.setScale(0.05)
        self.nodePath.setPos(
            random.uniform(0, 500),
            random.uniform(0, 500),
            random.uniform(0, 300)
        )
        self.tasks.append(self.act)

    # Override
    def act(self, task):
        """Main logic loop, overridden from BaseEntity"""
        # self.move(0, 0, -self.speed)
        # self.setHpr(self, self.rotation, 0, 0)
        # self.nodePath.setP(self.nodePath.getP() + 15)
        # self.addli
        return task.cont
    
    def move(self, x, y, z):
        """
        """
        pass
