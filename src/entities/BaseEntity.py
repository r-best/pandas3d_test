import random
import numpy as np
import math as math

from direct.actor.Actor import Actor
from panda3d.core import NodePath, CollisionNode, LineSegs
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

class BaseEntity(BulletRigidBodyNode):
    """
    """
    # Default entity model (overwritten by subclasses)
    MODEL = "models/teapot"
    # Field of view; how many degrees to the side the entity can see
    FOV = 180
    VIEW_DISTANCE = 1

    def __init__(self):
        self.ID = id(self)
        self.NAME = f"{type(self).__name__}_{self.ID}"
        super().__init__(self.NAME)
        # List of tasks to register to the Panda task manager
        self.tasks = (self.act,)
        self.nodePath = NodePath(self)
        self.nodePath.setTag('clickable', '1')
        self.actor = Actor(self.MODEL)
        self.actor.reparent_to(self.nodePath)
        self.setMass(1.0)

        # Set up actor position, hitbox, and other size-dependent properties
        self.setScale(1)
        
        self.nodePath.setPos(
            random.uniform(100, 400),
            random.uniform(0, 100),
            random.uniform(0, 150)
        )
    
    def onCollision(self, event):
        # print(event)
        pass

    def act(self, task):
        """Main logic loop for the entity, overridden in subclasses"""
        return task.cont
    
    def setScale(self, scale=1):
        """Resizes the entity and its hitbox to the desired scale
        """
        self.actor.setScale(scale)

        # Calculate model's size
        pt1, pt2 = self.actor.getTightBounds()
        self.width = pt2.getX() - pt1.getX()
        self.depth = pt2.getY() - pt1.getY()
        self.height = pt2.getZ() - pt1.getZ()

        # Reassign all size-dependent fields
        self.actor.setZ(-self.height/2)
        if self.getNumShapes() > 0: self.removeShape(self.getShape(0))
        self.addShape(BulletBoxShape((self.width/2, self.depth/2, self.height/2)))
        self.generateViewRays()

    def generateViewRays(self, numPoints=100):
        """https://youtu.be/bqtqltqcQhw?t=333
        """
        FIBONACCI = (1 + 5**0.5) / 2

        # Calculate length of collision lines based on
        # entity's size and view distance
        size = self.VIEW_DISTANCE * 1000 * self.actor.getScale()[0]

        ls = LineSegs()
        ls.setThickness(1)
        pointsColor = 0
        
        # Attach collision node that will hold all collision lines
        self.sightRayNP = self.nodePath.attachNewNode(CollisionNode(f"{self.NAME}_collisionRays"))
        self.sightRayNP.node().set_into_collide_mask(0)
        self.sightRayNP.setPos(self.sightRayNP, 0, -self.depth/2, self.height/2)
        self.sightRayNP.setHpr(0, 90, 0)

        for i in range(numPoints):
            inclination = math.acos(1 - 2*(i / (numPoints - 1)))
            azimuth = 2 * math.pi * FIBONACCI * i

            if (inclination / math.pi) > (self.FOV / 360):
                break

            x = math.sin(inclination) * math.cos(azimuth) * size
            y = math.sin(inclination) * math.sin(azimuth) * size
            z = math.cos(inclination) * size
        
            self.drawPoint(ls, x, y, z, (pointsColor, 0, 0, 1))
            pointsColor += 1/numPoints
        pointsNP = self.nodePath.attachNewNode(ls.create())
        pointsNP.setPos(pointsNP, 0, -self.depth/2, self.height/2)
        pointsNP.setHpr(0, 90, 0)

    def drawPoint(self, ls, x, y, z, color):
        """Draws a point at the specified coordinates relative
        to the entity, using the given LineSegs object, useful
        for debugging
        """
        ls.setColor(color)
        ls.moveTo(x, y, z)
        ls.drawTo(x+1, y, z)
        ls.drawTo(x-1, y, z)
        ls.moveTo(x, y, z)
        ls.drawTo(x, y+1, z)
        ls.drawTo(x, y-1, z)
        ls.moveTo(x, y, z)
        ls.drawTo(x, y, z+1)
        ls.drawTo(x, y, z-1)
