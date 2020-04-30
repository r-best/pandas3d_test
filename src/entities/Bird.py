import random

from direct.task import Task

from .BaseEntity import BaseEntity

class Bird(BaseEntity):
    """
    """
    MODEL = "models/panda-model"

    speed = 1
    rotation = 3

    def __init__(self):
        super().__init__()
        self.setScale(0.005)
        self.setPos(
            random.uniform(0, 50),
            random.uniform(0, 50),
            random.uniform(0, 30)
        )
        self.tasks.append(self.act)

    # Override
    def act(self, task):
        """Main logic loop, overridden from BaseEntity"""
        self.move(0, 0, -self.speed)
        # self.setHpr(self, self.rotation, 0, 0)
        self.setP(self.getP() + 15)
        return Task.cont
    
    def move(self, x, y, z):
        """
        """
        if z < 0 and self.getZ() + z < 0:
            z = -self.getZ()
        
        self.setPos(
            self.getX() + x,
            self.getY() + y,
            self.getZ() + z
        )
