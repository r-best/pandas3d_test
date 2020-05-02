from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import ClockObject, CollisionTraverser, CollisionFloorMesh, CollisionNode, CollisionHandlerFloor
from panda3d.physics import ForceNode, LinearVectorForce

from entities.Bird import Bird
from utils.Utils import rectangle


GRAVITY = 98.0

ENTITY_MAP = {
    "Bird": Bird
}

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
        # self.taskMgr.add(self.traverseTask, "tsk_traverse")

        # Render floor, for debugging
        # self.render.attachNewNode(rectangle('floor', 0, 0, 0, 50, 50))
        floorNP = render.attachNewNode(CollisionNode('floor'))
        floor = CollisionFloorMesh()
        floor.addVertex((0, 0, 0))
        floor.addVertex((500, 0, 0))
        floor.addVertex((0, 500, 0))
        floor.addVertex((500, 500, 0))
        floor.addTriangle(0, 1, 2)
        floor.addTriangle(3, 2, 1)
        print(floor.getNumTriangles())
        floorNP.node().addSolid(floor)
        
        # Establish gravity
        # gravityForce=LinearVectorForce(0, 0, -GRAVITY)
        # gravityFN=ForceNode('world-forces')
        # gravityFN.addForce(gravityForce)
        # gravityFNP=render.attachNewNode(gravityFN)
        # self.physicsMgr.addLinearForce(gravityForce)
        
        self.floorCollisionHandler = CollisionHandlerFloor()
        self.floorCollisionHandler.setMaxVelocity(GRAVITY)
    
    #** This is the loop periodically checked to find out if the have been collisions - it is fired by the taskMgr.add function set below.
    def traverseTask(self, task):
    # as soon as a collison is detected, the collision queue handler will contain all the objects taking part in the collison, but we must sort that list first, so to have the first INTO object collided then the second and so on. Of course here it is pretty useless 'cos there is just one INTO object to collide with in the scene but this is the way to go when there are many other.
        # self.floorCollisionHandler.sortEntries()
        # for i in range(self.floorCollisionHandler.getNumEntries()):
        #     entry = self.floorCollisionHandler.getEntry(i)
        #     print(f"COLLISION {i}")
        return task.cont

    def onclick(self):
        """
        """
        self.spawn_entity()
    
    def spawn_entity(self, entity_type="Bird"):
        """
        """
        entity = ENTITY_MAP[entity_type]()
        self.actors.append(entity)
        for task in entity.tasks:
            self.add_task(entity_type, entity.ID, task)
        entity.nodePath.reparent_to(self.render)
        self.physicsMgr.attachPhysicalNode(entity)
        self.floorCollisionHandler.addCollider(entity.floorFinder, entity.nodePath)
        self.cTrav.addCollider(entity.floorFinder, self.floorCollisionHandler)
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
