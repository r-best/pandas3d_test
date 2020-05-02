from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ClockObject, CollisionTraverser, CollisionNode, CollisionPlane, Plane
from panda3d.physics import ForceNode, LinearVectorForce, PhysicsCollisionHandler

from .utils import Utils


class World(ShowBase):

    actors = list()

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()
        self.setFrameRateMeter(True)

        # Register global events
        self.accept('mouse1', self.onclick)

        self.camera.setPos(250, -550, 200)
        self.camera.setHpr(0, -15, 0)
        
        self.enableParticles()
        self.cTrav = CollisionTraverser('collision_traverser')
        self.cTrav.showCollisions(self.render)
        self.taskMgr.add(self.traverseTask, "tsk_traverse")

        # Render floor, for debugging
        floorNP = render.attachNewNode(CollisionNode('floor'))
        floorNP.node().addSolid(CollisionPlane(Plane((0,0,0), (500,0,0), (0,500,0))))
        
        # Establish gravity
        gravityForce=LinearVectorForce(0, 0, -Utils.GRAVITY)
        gravityFN=ForceNode('world-forces')
        gravityFN.addForce(gravityForce)
        gravityFNP=render.attachNewNode(gravityFN)
        self.physicsMgr.addLinearForce(gravityForce)

        self.collisionHandler = PhysicsCollisionHandler()
    
    def traverseTask(self, task):
        for i in range(self.collisionHandler.getNumInPatterns()):
            entry = self.collisionHandler.getInPattern(i)
            print(f"IN COLLISION {i}")
        for i in range(self.collisionHandler.getNumOutPatterns()):
            entry = self.collisionHandler.getOutPattern(i)
            print(f"OUT COLLISION {i}")
        for i in range(self.collisionHandler.getNumAgainPatterns()):
            entry = self.collisionHandler.getAgainPattern(i)
            print(f"AGAIN COLLISION {i}")
        return task.cont

    def onclick(self):
        """
        """
        self.spawn_entity()
    
    def spawn_entity(self, entity_type="Bird"):
        """
        """
        entity = Utils.ENTITY_MAP[entity_type]()
        self.actors.append(entity)
        for task in entity.tasks:
            self.add_task(entity_type, entity.ID, task)
        entity.nodePath.reparent_to(self.render)
        self.physicsMgr.attachPhysicalNode(entity)
        self.collisionHandler.addCollider(entity.collisionBox, entity.nodePath)
        self.cTrav.addCollider(entity.collisionBox, self.collisionHandler)
        print(f"Spawned {entity_type} with ID {entity.ID}")
        return entity
    
    def add_task(self, entity_type, entity_id, func):
        """
        """
        self.taskMgr.add(func, f"{entity_type}_{entity_id}_{func.__name__}")


if __name__ == "__main__":
    ClockObject.getGlobalClock().setMode(ClockObject.MLimited)
    ClockObject.getGlobalClock().setFrameRate(60)
    World().run()
