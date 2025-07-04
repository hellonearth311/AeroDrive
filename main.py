from math import pi, sin, cos

from direct.showbase.ShowBase import *
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.gui.OnscreenText import OnscreenText


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.terrain = self.loader.loadModel("models/environment")
        self.terrain.reparentTo(self.render)

        self.terrain.setScale(0.5, 0.5, 0.5)
        self.terrain.setPos(0, 0, 0)

        # loading in and configuring the plane
        self.planeModel = self.loader.loadModel("assets/models/cessna-172.gltf")
        self.planeModel.reparentTo(self.render)

        self.planeModel.setScale(1.5, 1.5, 1.5)
        self.planeModel.setPos(0, 0, 50)
        
        # Set sky color
        self.setBackgroundColor(0.5, 0.8, 1.0, 1)

        # make the camera follow the plane at a fixed distance
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

        # handle all of the inputs
        self.accept("w", self.increase_throttle)
        self.accept("s", self.decrease_throttle)
        # self.accept("a", self.turn_left)
        # self.accept("d", self.turn_right)
        self.accept("arrow_up", self.pitch_up)
        self.accept("arrow_down", self.pitch_down)
        # self.accept("q", self.roll_left)
        # self.accept("e", self.roll_right)

        # Create HUD elements
        self.throttle_text = OnscreenText(text="Throttle: 0%", pos=(-1.3, 0.9), scale=0.07, fg=(1, 1, 1, 1))
        self.speed_text = OnscreenText(text="Speed: 0", pos=(-1.3, 0.8), scale=0.07, fg=(1, 1, 1, 1))
        self.altitude_text = OnscreenText(text="Alt: 0", pos=(-1.3, 0.7), scale=0.07, fg=(1, 1, 1, 1))
        self.pitch_text = OnscreenText(text="Pitch: 0", pos=(-1.3, 0.6), scale=0.07, fg=(1, 1, 1, 1))
        self.position_text = OnscreenText(text="Pos: 0,0,0", pos=(-1.3, 0.5), scale=0.07, fg=(1, 1, 1, 1))

        self.taskMgr.add(self.update_physics, "update_physics")

    # semi realistic physics (actually proud of ts)
    def update_physics(self, task):
        dt = globalClock.getDt()

        pitch_rad = self.pitch * (pi / 180)
        
        thrust = self.throttle * -100
        
        speed = self.velocity.length()
        
        max_forward_speed = 120
        max_climb_rate = 16

        base_lift = thrust * 0.3
        pitch_lift = speed * 5 * sin(pitch_rad)
        total_lift = base_lift + pitch_lift
        
        drag = speed * speed * 0.02 + speed * 1.5

        forward_force = thrust - drag
        vertical_force = total_lift - 3.0 

        self.velocity.y += forward_force * dt
        self.velocity.z += vertical_force * dt
        
        if abs(self.velocity.y) > max_forward_speed:
            self.velocity.y = max_forward_speed if self.velocity.y > 0 else -max_forward_speed

        if self.velocity.z > max_climb_rate:
            self.velocity.z = max_climb_rate
        elif self.velocity.z < -max_climb_rate * 1.5:
            self.velocity.z = -max_climb_rate * 1.5

        self.velocity.y *= 0.98
        self.velocity.z *= 0.995
        self.velocity.x *= 0.98
        
        new_pos = self.planeModel.getPos() + self.velocity * dt
        self.planeModel.setPos(new_pos)

        current_hpr = self.planeModel.getHpr()
        self.planeModel.setHpr(current_hpr.x, -self.pitch, current_hpr.z)
        
        actual_speed = self.velocity.length()
        climb_rate = self.velocity.z

        self.throttle_text.setText(f"Throttle: {self.throttle*100:.0f}%")
        self.speed_text.setText(f"Speed: {actual_speed:.1f} | Climb: {climb_rate:.1f}")
        self.altitude_text.setText(f"Alt: {new_pos.z:.1f}")
        self.pitch_text.setText(f"Pitch: {self.pitch:.0f}°")
        self.position_text.setText(f"Pos: {new_pos.x:.0f},{new_pos.y:.0f},{new_pos.z:.0f}")

        return task.cont
    # plane control
    def increase_throttle(self):
        self.throttle = min(1.0, self.throttle + 0.1)

    def decrease_throttle(self):
        self.throttle = max(0.0, self.throttle - 0.1)

    def pitch_up(self):
        self.pitch = min(30, self.pitch + 5)

    def pitch_down(self):
        self.pitch = max(-30, self.pitch - 5)


app = MyApp()
app.run()