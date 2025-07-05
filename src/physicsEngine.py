from math import pi, sin, cos, radians, sqrt, exp, atan2, degrees

# simple physics (actually works)
def update_physics(globalClock, planeModel, pitch, yaw, throttle, velocity, roll, throttle_text, speed_text, altitude_text, pitch_text, position_text):
    dt = globalClock.getDt()

    pitch_rad = radians(pitch)
    yaw_rad = radians(yaw)
    
    thrust = throttle * 50
    
    speed = velocity.length()
    
    max_forward_speed = 300
    max_climb_rate = 16

    base_lift = thrust * 0.3
    pitch_lift = speed * 5 * sin(pitch_rad)
    total_lift = base_lift + pitch_lift
    
    drag = speed * speed * 0.02 + speed * 1.5

    forward_force = thrust - drag
    vertical_force = total_lift - 3.0 

    # Apply thrust in the direction the plane is facing
    velocity.x += forward_force * sin(yaw_rad) * dt
    velocity.y += forward_force * -cos(yaw_rad) * dt
    velocity.z += vertical_force * dt
    
    # Apply speed limits
    horizontal_speed = (velocity.x ** 2 + velocity.y ** 2) ** 0.5
    if horizontal_speed > max_forward_speed:
        scale = max_forward_speed / horizontal_speed
        velocity.x *= scale
        velocity.y *= scale

    if velocity.z > max_climb_rate:
        velocity.z = max_climb_rate
    elif velocity.z < -max_climb_rate * 1.5:
        velocity.z = -max_climb_rate * 1.5

    velocity.y *= 0.98
    velocity.z *= 0.995
    velocity.x *= 0.98
    
    new_pos = planeModel.getPos() + velocity * dt
    planeModel.setPos(new_pos)

    planeModel.setHpr(yaw, -pitch, roll)
    
    actual_speed = velocity.length()
    climb_rate = velocity.z

    throttle_text.setText(f"Throttle: {throttle*100:.0f}%")
    speed_text.setText(f"Speed: {actual_speed:.1f} | Climb: {climb_rate:.1f}")
    altitude_text.setText(f"Alt: {new_pos.z:.1f}")
    pitch_text.setText(f"Pitch: {pitch:.0f}°")
    position_text.setText(f"Pos: {new_pos.x:.0f},{new_pos.y:.0f},{new_pos.z:.0f}")