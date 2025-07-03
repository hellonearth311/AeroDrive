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

        # an actor is a model with animations
        # we can load it in like this
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        
        # now we load it in like a normal model and make it loop the walking animation
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        self.pandaActor.loop("walk")

        # let me try loading in a plane
        self.planeModel = self.loader.loadModel("assets/models/plane.egg")
        self.planeModel.reparentTo(self.render)

        self.planeModel.setScale(4, 4, 4)

    def spinCameraTask(self, task):
        # tasks are functions that will be called every frame
        # this task spins the camera around using some fancy math i dont quite understand
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()