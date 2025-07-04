from math import pi, sin, cos, radians

from direct.showbase.ShowBase import *
from direct.task import Task
from panda3d.core import Vec3
from direct.gui.OnscreenText import OnscreenText

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

        self.velocity = Vec3(0, 0, 0)
        self.angular_velocity = Vec3(0, 0, 0)
        self.throttle = 0.5
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0

        self.mass = 1000
        self.gravity = -3.0  # Reduced gravity for better realism in simulation
        self.lift_coefficient = 1.5
        self.drag_coefficient = 0.03
        self.thrust_power = 3000
        self.area = 16

        self.accept("w", self.increase_throttle)
        self.accept("s", self.decrease_throttle)
        self.accept("a", self.turn_left)
        self.accept("d", self.turn_right)
        self.accept("arrow_up", self.pitch_up)
        self.accept("arrow_down", self.pitch_down)
        self.accept("q", self.roll_left)
        self.accept("e", self.roll_right)

        self.throttle_text = OnscreenText(text="Throttle: 0%", pos=(-1.3, 0.9), scale=0.07)
        self.speed_text = OnscreenText(text="Speed: 0", pos=(-1.3, 0.8), scale=0.07)
        self.altitude_text = OnscreenText(text="Alt: 0", pos=(-1.3, 0.7), scale=0.07)
        self.pitch_text = OnscreenText(text="Pitch: 0", pos=(-1.3, 0.6), scale=0.07)
        self.position_text = OnscreenText(text="Pos: 0,0,0", pos=(-1.3, 0.5), scale=0.07)

        self.taskMgr.add(self.update_physics, "update_physics")

    def update_physics(self, task):
        dt = globalClock.getDt()
        pitch_rad = radians(self.pitch)
        yaw_rad = radians(self.yaw)

        forward = Vec3(sin(yaw_rad), -cos(yaw_rad), 0)
        upward = Vec3(0, 0, 1)

        thrust_force = forward * (self.throttle * self.thrust_power)

        speed = self.velocity.length()
        lift_force = upward * (0.5 * 1.225 * speed ** 2 * self.area * self.lift_coefficient)

        drag_force = -self.velocity.normalized() * (0.5 * 1.225 * speed ** 2 * self.area * self.drag_coefficient) if speed > 0 else Vec3(0, 0, 0)

        gravity_force = Vec3(0, 0, self.mass * self.gravity)

        total_force = thrust_force + lift_force + drag_force + gravity_force

        acceleration = total_force / self.mass
        self.velocity += acceleration * dt

        new_pos = self.planeModel.getPos() + self.velocity * dt
        self.planeModel.setPos(new_pos)

        self.planeModel.setHpr(self.yaw, -self.pitch, self.roll)

        self.throttle_text.setText(f"Throttle: {self.throttle*100:.0f}%")
        self.speed_text.setText(f"Speed: {speed:.1f} m/s")
        self.altitude_text.setText(f"Alt: {new_pos.z:.1f} m")
        self.pitch_text.setText(f"Pitch: {self.pitch:.0f}°")
        self.position_text.setText(f"Pos: {new_pos.x:.0f},{new_pos.y:.0f},{new_pos.z:.0f}")

        return task.cont

    def increase_throttle(self):
        self.throttle = min(1.0, self.throttle + 0.05)

    def decrease_throttle(self):
        self.throttle = max(0.0, self.throttle - 0.05)

    def pitch_up(self):
        self.pitch += 2

    def pitch_down(self):
        self.pitch -= 2

    def roll_right(self):
        self.roll -= 2

    def roll_left(self):
        self.roll += 2

    def turn_left(self):
        self.yaw -= 2

    def turn_right(self):
        self.yaw += 2

app = MyApp()
app.run()
