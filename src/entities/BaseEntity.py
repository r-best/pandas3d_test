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
    # Field of view; how many degrees to the side the entity can see
    FOV = 180
    VIEW_DISTANCE = 1

    def __init__(self):
        self.ID = id(self)
        self.NAME = f"{type(self).__name__}_{self.ID}"
        super().__init__(self.NAME)
        self.setTag('clickable', '1')
        # List of tasks to register to the Panda task manager
        self.tasks = (self.act,)
        self.nodePath = NodePath(self)
        self.actor = Actor(self.MODEL)
        self.actor.reparent_to(self.nodePath)
        
        # Set up hitbox
        self.calculateDims()
        self.collisionBox = self.nodePath.attachNewNode(CollisionNode(f'{self.NAME}_collisionBox'))
        self.collisionBox.node().addSolid(CollisionBox((0,0,self.height/2), self.width/2, self.depth/2, self.height/2))
        # self.collisionBox.show()
        
        self.actor.accept(f"in-{self.collisionBox.node().name}", self.onCollision)
        self.actor.accept(f'again-{self.collisionBox.node().name}', self.onCollision)
        self.actor.accept(f'out-{self.collisionBox.node().name}', self.onCollision)
        
        self.nodePath.setPos(
            random.uniform(0, 300),
            random.uniform(0, 100),
            random.uniform(0, 150)
        )

        self.getPhysicsObject().setVelocity(0,0,80)
        # self.generateViewRays()
    
    def onCollision(self, event):
        print(event)

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
        """Recalculates the entity's dimensions and stores
        them in the respective class fields (`self.width`,
        `self.depth`, and `self.height`)
        Should not need to be called unless you're modifying
        the entity's size without using `self.setScale()`
        """
        pt1, pt2 = self.nodePath.getTightBounds()
        self.width = pt2.getX() - pt1.getX()
        self.depth = pt2.getY() - pt1.getY()
        self.height = pt2.getZ() - pt1.getZ()

    def generateViewRays(self, numPoints=1000):
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
        self.sightRayNP.setPos(rayNP, 0, -self.depth/2, self.height/2)
        self.sightRayNP.setHpr(0, 90, 0)

        for i in range(numPoints):
            inclination = Math.acos(1 - 2*(i / (numPoints - 1)))
            azimuth = 2 * Math.pi * FIBONACCI * i

            if (inclination / Math.pi) < (self.FOV / 360):
                x = Math.sin(inclination) * Math.cos(azimuth) * size
                y = Math.sin(inclination) * Math.sin(azimuth) * size
                z = Math.cos(inclination) * size
            
                self.drawPoint(ls, x, y, z, (pointsColor, 0, 0, 1))
                pointsColor += 1/numPoints
                self.sightRayNP.node().addSolid(CollisionSegment(0, 0, 0, x, y, z))
                # self.sightRayNP.show()
                self.sightRayNP.node().getSolid
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
