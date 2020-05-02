from direct.actor.Actor import Actor
from panda3d.core import NodePath, CollisionBox, CollisionNode, CollisionHandlerFloor, CollisionRay
from panda3d.physics import ActorNode

class BaseEntity(ActorNode):
    """
    """
    # Default entity model (overwritten by subclasses)
    MODEL = "models/teapot"

    def __init__(self):
        self.ID = id(self)
        super().__init__(f"{type(self).__name__}_{self.ID}_physnode")
        self.tasks = list()
        self.nodePath = NodePath(self)
        self.actor = Actor(self.MODEL)
        self.actor.reparent_to(self.nodePath)

        floorFinderCN = CollisionNode(f'{type(self).__name__}_{self.ID}_floorCollider')
        floorFinderCN.setIntoCollideMask(0)
        self.floorFinder = self.nodePath.attachNewNode(floorFinderCN)
        self.floorFinder.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
