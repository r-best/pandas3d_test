import random

from direct.actor.Actor import Actor
from panda3d.core import NodePath, CollisionNode, CollisionBox
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
        
        # Set up hitbox
        pt1, pt2 = self.nodePath.getTightBounds()
        width = pt2.getX() - pt1.getX()
        depth = pt2.getY() - pt1.getY()
        height = pt2.getZ() - pt1.getZ()
        self.collisionBox = self.nodePath.attachNewNode(CollisionNode(f'{type(self).__name__}_{self.ID}_collisionBox'))
        self.collisionBox.node().addSolid(CollisionBox((0,0,height/2), width/2, depth/2, height/2))
        self.collisionBox.show()
        
        self.nodePath.setPos(
            random.uniform(0, 500),
            random.uniform(0, 500),
            random.uniform(0, 300)
        )

        self.getPhysicsObject().setVelocity(0,0,80)
    
    def setScale(self, scale=1):
        """Resizes the entity and its hitbox to the desired scale
        """
        self.actor.setScale(scale)
        self.collisionBox.setScale(scale)

    def act(self, task):
        """Main logic loop for the entity, overridden in subclasses"""
        return task.cont
