from math import pi, sin, cos

from direct.showbase.ShowBase import *
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.gui.OnscreenText import OnscreenText


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # loading in and configuring the plane
        self.planeModel = self.loader.loadModel("assets/models/C172.glb")
        self.planeModel.reparentTo(self.render)

        self.planeModel.setScale(1.5, 1.5, 1.5)
        self.planeModel.setPos(0, 0, 50)

        # Create simple terrain
        from panda3d.core import CardMaker
        cm = CardMaker("ground")
        cm.setFrame(-1000, 1000, -1000, 1000)
        self.terrain = self.render.attachNewNode(cm.generate())
        self.terrain.setPos(0, 0, 0)
        self.terrain.setScale(0.25, 0.25, 0.25)
        
        # Add some reference cubes to see movement
        for i in range(10):
            for j in range(10):
                cube = self.loader.loadModel("models/environment")
                if not cube:
                    # Create simple cube if environment model doesn't exist
                    from panda3d.core import CardMaker
                    cm_cube = CardMaker("cube")
                    cm_cube.setFrame(-1, 1, -1, 1)
                    cube = self.render.attachNewNode(cm_cube.generate())
                    cube.setColor(0.8, 0.4, 0.2, 1)  # Brown cubes
                
                cube.reparentTo(self.render)
                cube.setPos(i * 50 - 250, j * 50 - 250, 2)
                cube.setScale(5, 5, 5)
        
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

    def update_physics(self, task):
        dt = globalClock.getDt()

        pitch_rad = self.pitch * (pi / 180)
        
        # Much stronger thrust
        thrust = self.throttle * 200
        
        speed = self.velocity.length()
        
        # Better lift calculation - works even at low speeds
        base_lift = thrust * 0.3  # Basic lift from forward motion
        pitch_lift = speed * 5 * sin(pitch_rad)  # Additional lift from pitch
        total_lift = base_lift + pitch_lift
        
        # Reduced drag
        drag = speed * 0.5
        
        # Apply forces
        forward_force = thrust - drag
        vertical_force = total_lift - 1.0  # Much weaker gravity
        
        # Update velocity
        self.velocity.y += forward_force * dt
        self.velocity.z += vertical_force * dt
        
        # Less damping
        self.velocity *= 0.995
        
        # Update position
        new_pos = self.planeModel.getPos() + self.velocity * dt
        self.planeModel.setPos(new_pos)

        current_hpr = self.planeModel.getHpr()
        self.planeModel.setHpr(current_hpr.x, -self.pitch, current_hpr.z)
        
        # Update HUD
        self.throttle_text.setText(f"Throttle: {self.throttle*100:.0f}%")
        self.speed_text.setText(f"Speed: {speed:.1f}")
        self.altitude_text.setText(f"Alt: {new_pos.z:.1f}")
        self.pitch_text.setText(f"Pitch: {self.pitch:.0f}°")
        self.position_text.setText(f"Pos: {new_pos.x:.0f},{new_pos.y:.0f},{new_pos.z:.0f}")
        
        return task.cont
    
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