from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ClockObject, CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay, CollisionPlane, Plane, GeomNode, CollisionHandlerPusher
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
        self.accept('mouse3', self.spawn_entity)

        # Enable physics and collision
        self.enableParticles()
        self.collisionHandler = PhysicsCollisionHandler()
        self.collisionHandler.addInPattern('%fn-in-%in')
        self.collisionHandler.addAgainPattern('%fn-again-%in')
        self.collisionHandler.addOutPattern('%fn-out-%in')
        self.cTrav = CollisionTraverser('collision_traverser')
        # self.cTrav.showCollisions(self.render)
        self.taskMgr.add(self.traverseTask, "tsk_traverse")

        # Set up camera
        self.camera.setPos(250, -550, 200)
        self.camera.setHpr(0, -15, 0)
        self.cameraCollisionHandler = CollisionHandlerQueue()
        self.cameraRay = CollisionRay()
        cameraRayNode = CollisionNode('mouseRay')
        cameraRayNode.setIntoCollideMask(0)
        cameraRayNode.addSolid(self.cameraRay)
        cameraRayNp = self.camera.attachNewNode(cameraRayNode)
        self.cTrav.addCollider(cameraRayNp, self.cameraCollisionHandler)

        # Render floor, for debugging
        floorNP = render.attachNewNode(CollisionNode('floor'))
        floorNP.node().addSolid(CollisionPlane(Plane((0,0,0), (1,0,0), (0,1,0))))
        
        # Establish gravity
        gravityForce = LinearVectorForce(0, 0, -Utils.GRAVITY)
        gravityFN = ForceNode('world-forces')
        gravityFN.addForce(gravityForce)
        gravityFNP = render.attachNewNode(gravityFN)
        self.physicsMgr.addLinearForce(gravityForce)

    def onclick(self):
        """
        """
        # First we check that the mouse is not outside the screen.
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.cameraRay.setFromLens(self.camNode, mpos.x, mpos.y)

            self.cTrav.traverse(self.render)
            if self.cameraCollisionHandler.getNumEntries() > 0:
                self.cameraCollisionHandler.sortEntries()
                pickedObj = self.cameraCollisionHandler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('clickable')
                if not pickedObj.isEmpty():
                    pickedObj.node().getPhysicsObject().setVelocity(0,100,300)
    
    def traverseTask(self, task):
        # print(f"NUM IN {self.collisionHandler.getNumInPatterns()}")
        # print(f"NUM OUT {self.collisionHandler.getNumOutPatterns()}")
        # print(f"NUM AGAIN {self.collisionHandler.getNumAgainPatterns()}")
        # for i in range(self.collisionHandler.getNumInPatterns()):
        #     entry = self.collisionHandler.getInPattern(i)
        #     print(f"IN COLLISION {i}")
        # for i in range(self.collisionHandler.getNumOutPatterns()):
        #     entry = self.collisionHandler.getOutPattern(i)
        #     print(f"OUT COLLISION {i}")
        # for i in range(self.collisionHandler.getNumAgainPatterns()):
        #     entry = self.collisionHandler.getAgainPattern(i)
        #     print(f"AGAIN COLLISION {i}")
        return task.cont
    
    def spawn_entity(self, entity_type="Bird"):
        """
        """
        entity = Utils.ENTITY_MAP[entity_type]()
        self.actors.append(entity)
        for task in entity.tasks:
            self.add_task(entity_type, entity.ID, task)
        entity.nodePath.reparent_to(self.render)
        self.physicsMgr.attachPhysicalNode(entity)
        self.cTrav.addCollider(entity.collisionBox, self.collisionHandler)
        self.collisionHandler.addCollider(entity.collisionBox, entity.nodePath)
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
