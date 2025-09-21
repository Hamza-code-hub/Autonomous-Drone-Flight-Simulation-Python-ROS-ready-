# src/controller.py
import numpy as np

class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt=0.1, max_speed=3.0, repulsion_gain=1.2, repulsion_radius=4.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.max_speed = max_speed
        self.int_err = np.array([0.0, 0.0])
        self.prev_err = None
        # simple inter-drone repulsion parameters
        self.repulsion_gain = repulsion_gain
        self.repulsion_radius = repulsion_radius

    def compute(self, drone, target, neighbors=None):
        """
        Compute vx, vy to move toward target.
        If neighbors provided (list of (x,y)), apply repulsive velocity to avoid collisions.
        """
        pos = np.array([drone.x, drone.y])
        target = np.array(target)
        err = target - pos
        self.int_err += err * self.dt
        if self.prev_err is None:
            der = np.array([0.0, 0.0])
        else:
            der = (err - self.prev_err) / self.dt
        self.prev_err = err

        u = self.kp * err + self.ki * self.int_err + self.kd * der

        # repulsive term from neighbors
        if neighbors:
            for npos in neighbors:
                nv = np.array(npos)
                diff = pos - nv
                dist = np.linalg.norm(diff)
                if dist < 1e-6:
                    continue
                if dist < self.repulsion_radius:
                    # repulsive vector magnitude ~ (1/dist - 1/r) scaled
                    # simpler: linear repulsion
                    rep_strength = self.repulsion_gain * (self.repulsion_radius - dist) / self.repulsion_radius
                    u += (diff / dist) * rep_strength

        # clamp speed
        speed = np.linalg.norm(u)
        if speed > self.max_speed:
            u = u / speed * self.max_speed
        return float(u[0]), float(u[1])
