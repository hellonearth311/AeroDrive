from direct.showbase.ShowBase import *
from direct.task import Task
from panda3d.core import Vec3, CollisionNode, CollisionSphere, CollisionTraverser, CollisionHandlerEvent, CollisionBox
from direct.gui.OnscreenText import OnscreenText

from terrainEngine import update_terrain
from physicsEngine import update_physics

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.terrain = self.loader.loadModel("models/environment")
        self.terrain.reparentTo(self.render)
        self.terrain.setScale(0.5)
        self.terrain.setPos(0, 0, 0)

        self.planeModel = self.loader.loadModel("assets/models/C172.glb")
        self.planeModel.reparentTo(self.render)
        self.planeModel.setScale(1.5)
        self.planeModel.setPos(0, 0, 50)

        self.setBackgroundColor(0.5, 0.8, 1.0, 1)

        self.disableMouse()
        self.camera.reparentTo(self.planeModel)
        self.camera.setPos(0, 30, 10)
        self.camera.lookAt(0, 0, 0)

        # flight physics variables
        self.velocity = Vec3(0, 0, 0)
        self.angular_velocity = Vec3(0, 0, 0)
        self.throttle = 0.5  # Start with 50% throttle
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0

        # terrain var
        self.loaded_chunks = {}

        # collision
        self.cTrav = CollisionTraverser()
        
        self.collision_handler = CollisionHandlerEvent()
        self.collision_handler.addInPattern('%fn-into-%in')

        # plane collision sphere
        plane_cnode = CollisionNode('plane')
        plane_cnode.addSolid(CollisionSphere(0, 0, 0, 5))

        self.plane_cnodepath = self.planeModel.attachNewNode(plane_cnode)
        
        self.cTrav.addCollider(self.plane_cnodepath, self.collision_handler)

        # terrain collision box
        terrain_cnode = CollisionNode('terrain')
        terrain_cnode.addSolid(CollisionBox((0, 0, 0), 500, 500, 10))
        
        self.terrain_cnodepath = self.terrain.attachNewNode(terrain_cnode)

        # accept collision
        self.accept('plane-into-terrain', self.on_plane_collision)

        self.throttle_text = OnscreenText(text="Throttle: 0%", pos=(-1.2, 0.9), scale=0.07)
        self.speed_text = OnscreenText(text="Speed: 0", pos=(-1.2, 0.8), scale=0.07)
        self.altitude_text = OnscreenText(text="Alt: 0", pos=(-1.2, 0.7), scale=0.07)
        self.pitch_text = OnscreenText(text="Pitch: 0", pos=(-1.2, 0.6), scale=0.07)
        self.position_text = OnscreenText(text="Pos: 0,0,0", pos=(-1.2, 0.5), scale=0.07)

        self.taskMgr.add(self.update_physics_task, "update_physics")
        self.taskMgr.add(self.check_inputs, "check_inputs")
        self.taskMgr.add(self.update_terrain_task, "update_terrain")
        self.taskMgr.add(self.collision_task, "collision")
    
    def check_inputs(self, task):
        if self.mouseWatcherNode.isButtonDown("w"):
            self.increase_throttle()
        elif self.mouseWatcherNode.isButtonDown("s"):
            self.decrease_throttle()
        elif self.mouseWatcherNode.isButtonDown("a"):
            self.turn_left()
        elif self.mouseWatcherNode.isButtonDown("d"):
            self.turn_right()
        elif self.mouseWatcherNode.isButtonDown("arrow_up"):
            self.pitch_up()
        elif self.mouseWatcherNode.isButtonDown("arrow_down"):
            self.pitch_down()
        elif self.mouseWatcherNode.isButtonDown("q"):
            self.roll_left()
        elif self.mouseWatcherNode.isButtonDown("e"):
            self.roll_right()
        
        return task.cont

    def update_terrain_task(self, task):
        update_terrain(self.loaded_chunks, self.planeModel, self.loader, self.render)
        return task.cont

    def update_physics_task(self, task):
        update_physics(globalClock, self.planeModel, 
                       self.pitch, self.yaw, self.throttle, self.velocity, self.roll, 
                       self.throttle_text, self.speed_text, self.altitude_text, self.pitch_text, self.position_text)
        return task.cont

    def collision_task(self, task):
        self.cTrav.traverse(self.render)
        return task.cont

    def on_plane_collision(self, entry):
        self.planeModel.setPos(0, 50, 0)

    # plane control
    def increase_throttle(self):
        self.throttle = min(1.0, self.throttle + 0.01)

    def decrease_throttle(self):
        self.throttle = max(0.0, self.throttle - 0.01)

    def pitch_up(self):
        self.pitch += 1

    def pitch_down(self):
        self.pitch -= 1
    
    def roll_right(self):
        self.roll -= 1
    
    def roll_left(self):
        self.roll += 1
    
    def turn_left(self):
        self.yaw += 1
    
    def turn_right(self):
        self.yaw -= 1

app = MyApp()
app.run()
