from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import ClockObject, Point3
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletPlaneShape, BulletDebugNode

from .utils import Utils


class World(ShowBase):

    actors = list()

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()
        self.setFrameRateMeter(True)

        # Set up camera
        self.camera.setPos(250, -550, 200)
        self.camera.setHpr(0, -15, 0)

        # Register global events
        self.accept('mouse1', self.onclick)
        self.accept('mouse3', self.spawn_entity)

        # Enable physics and collision
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()
        self.world = BulletWorld()
        self.world.setGravity((0, 0, -981.00))
        self.world.setDebugNode(debugNP.node())
        self.taskMgr.add(self.update, "physics_update")

        # Render floor, for debugging
        node = BulletRigidBodyNode('floor')
        node.addShape(BulletPlaneShape((0, 0, 1), 0))
        self.render.attachNewNode(node)
        self.world.attachRigidBody(node)
        
        node = BulletRigidBodyNode('wall-left')
        node.addShape(BulletPlaneShape((1, 0, 0), 100))
        self.render.attachNewNode(node)
        self.world.attachRigidBody(node)
        
        node = BulletRigidBodyNode('wall-right')
        node.addShape(BulletPlaneShape((-1, 0, 0), -400))
        self.render.attachNewNode(node)
        self.world.attachRigidBody(node)
        
        node = BulletRigidBodyNode('wall-down')
        node.addShape(BulletPlaneShape((0, 1, 0), 0))
        self.render.attachNewNode(node)
        self.world.attachRigidBody(node)
        
        node = BulletRigidBodyNode('wall-up')
        node.addShape(BulletPlaneShape((0, -1, 0), -300))
        self.render.attachNewNode(node)
        self.world.attachRigidBody(node)
    
    def update(self, task):
        """
        """
        dt = ClockObject.getGlobalClock().getDt()
        self.world.doPhysics(dt)
        return task.cont

    def onclick(self):
        """
        """
        # First we check that the mouse is not outside the screen.
        if base.mouseWatcherNode.hasMouse():
            pMouse = base.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            base.camLens.extrude(pMouse, pFrom, pTo)

            # Transform to global coordinates
            pFrom = render.getRelativePoint(base.cam, pFrom)
            pTo = render.getRelativePoint(base.cam, pTo)

            obj = self.world.rayTestClosest(pFrom, pTo)
            obj.getNode().setLinearVelocity((500,0,0))
    
    def spawn_entity(self, entity_type="Bird"):
        """
        """
        entity = Utils.ENTITY_MAP[entity_type]()
        self.actors.append(entity)
        for task in entity.tasks:
            self.add_task(entity_type, entity.ID, task)
        entity.nodePath.reparent_to(self.render)
        self.world.attachRigidBody(entity)
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
