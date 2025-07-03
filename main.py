from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # load the environment model
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)

        # place and set the scale of the environment model
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # to make a task work, you need to add it to the task manager
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # let me try loading in a plane
        self.planeModel = self.loader.loadModel("assets/models/C172.glb")
        self.planeModel.reparentTo(self.render)

        self.planeModel.setScale(1.5, 1.5, 1.5)
        self.planeModel.setPos(0, 0, 4)

    def spinCameraTask(self, task):
        # tasks are functions that will be called every frame
        # this task spins the camera around using some fancy math i dont quite understand
        angleDegrees = task.time * 12.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()