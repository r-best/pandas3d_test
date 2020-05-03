import math as Math
import random

from direct.actor.Actor import Actor
from panda3d.core import NodePath, CollisionNode, CollisionBox, CollisionSegment, LineSegs
from panda3d.physics import ActorNode

class BaseEntity(ActorNode):
    """
    """
    # Default entity model (overwritten by subclasses)
    MODEL = "models/teapot"

    def __init__(self):
        self.ID = id(self)
        super().__init__(f"{type(self).__name__}_{self.ID}_physnode")
        # List of tasks to register to the Panda task manager
        self.tasks = (
            self.act,
        )
        self.nodePath = NodePath(self)
        self.actor = Actor(self.MODEL)
        self.actor.reparent_to(self.nodePath)
        self.setTag('clickable', '1')
        
        # Set up hitbox
        self.calculateDims()
        self.collisionBox = self.nodePath.attachNewNode(CollisionNode(f'{type(self).__name__}_{self.ID}_collisionBox'))
        self.collisionBox.node().addSolid(CollisionBox((0,0,self.height/2), self.width/2, self.depth/2, self.height/2))
        self.collisionBox.show()
        
        self.nodePath.setPos(
            random.uniform(0, 500),
            random.uniform(0, 500),
            random.uniform(0, 150)
        )

        self.getPhysicsObject().setVelocity(0,0,80)
        # self.generateViewRays()

    def act(self, task):
        """Main logic loop for the entity, overridden in subclasses"""
        return task.cont
    
    def setScale(self, scale=1):
        """Resizes the entity and its hitbox to the desired scale
        """
        self.actor.setScale(scale)
        self.collisionBox.setScale(scale)
        self.calculateDims()
        self.generateViewRays()
    
    def calculateDims(self):
        """
        """
        pt1, pt2 = self.nodePath.getTightBounds()
        self.width = pt2.getX() - pt1.getX()
        self.depth = pt2.getY() - pt1.getY()
        self.height = pt2.getZ() - pt1.getZ()

    def generateViewRays(self, numPoints=150):
        """https://youtu.be/bqtqltqcQhw?t=333
        """
        size = 1000 * self.actor.getScale()[0]
        rayNP = self.nodePath.attachNewNode(CollisionNode('collisionrays'))
        rayNP.node().set_into_collide_mask(0)
        rayNP.setPos(rayNP, 0, 0, self.height/2)
        for i in range(numPoints):
            inclination = Math.acos(1 - 2*(i / (numPoints - 1)))
            azimuth = 2 * Math.pi * 0.618033 * i

            x = Math.sin(inclination) * Math.cos(azimuth) * size
            y = Math.sin(inclination) * Math.sin(azimuth) * size
            z = Math.cos(inclination) * size

            rayNP.node().addSolid(CollisionSegment(0, 0, 0, x, y, z))
            rayNP.show()
