import math

class Drone:
    """Simple 2D point-mass drone with velocity control."""
    def __init__(self, x=0.0, y=0.0, yaw=0.0, max_speed=5.0):
        self.x = float(x)
        self.y = float(y)
        self.yaw = float(yaw)
        self.max_speed = float(max_speed)
        self.history = []

    def step(self, vx_cmd, vy_cmd, dt):
        speed = (vx_cmd**2 + vy_cmd**2)**0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            vx_cmd *= scale
            vy_cmd *= scale

        self.x += vx_cmd * dt
        self.y += vy_cmd * dt
        if speed > 0.001:
            self.yaw = math.atan2(vy_cmd, vx_cmd)
        self.history.append((self.x, self.y))
