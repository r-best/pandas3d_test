from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import ClockObject

from entities.Bird import Bird
from utils.Utils import rectangle


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

        self.camera.setPos(25, -60, 25)
        self.camera.setHpr(0, -15, 0)

        # Render floor, for debugging
        self.render.attachNewNode(rectangle('floor', 0, 0, 0, 50, 50))
    
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
            self.add_task(entity_type, id(entity), task)
        print(f"Spawned {entity_type} with ID {id(entity)}")
        entity.reparent_to(self.render)
        return entity
    
    def add_task(self, entity_type, entity_id, func):
        """
        """
        self.taskMgr.add(func, f"{entity_type}_{entity_id}_{func.__name__}")

    

if __name__ == "__main__":
    ClockObject.getGlobalClock().setMode(ClockObject.MLimited)
    ClockObject.getGlobalClock().setFrameRate(60)
    World().run()
