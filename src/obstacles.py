# src/obstacles.py
import numpy as np
import math
import random

class ObstacleMap:
    def __init__(self, grid_size=(60, 40), resolution=1.0):
        # grid_size: (width, height)
        self.grid_size = grid_size
        self.resolution = resolution
        self.occ = np.zeros(grid_size, dtype=bool)
        # keep lists for visualization
        self.rects = []
        self.circles = []

    def add_rect(self, rect):
        """rect: (x_min, y_min, x_max, y_max) in meters"""
        x_min, y_min, x_max, y_max = rect
        ix_min = int(math.floor(x_min / self.resolution))
        iy_min = int(math.floor(y_min / self.resolution))
        ix_max = int(math.floor(x_max / self.resolution))
        iy_max = int(math.floor(y_max / self.resolution))
        ix_min = max(0, ix_min)
        iy_min = max(0, iy_min)
        ix_max = min(self.grid_size[0]-1, ix_max)
        iy_max = min(self.grid_size[1]-1, iy_max)
        self.occ[ix_min:ix_max+1, iy_min:iy_max+1] = True
        self.rects.append((x_min, y_min, x_max, y_max))

    def add_circle(self, circle):
        """circle: (cx, cy, radius) in meters"""
        cx, cy, r = circle
        ix_min = int(math.floor((cx - r) / self.resolution))
        iy_min = int(math.floor((cy - r) / self.resolution))
        ix_max = int(math.floor((cx + r) / self.resolution))
        iy_max = int(math.floor((cy + r) / self.resolution))
        ix_min = max(0, ix_min)
        iy_min = max(0, iy_min)
        ix_max = min(self.grid_size[0]-1, ix_max)
        iy_max = min(self.grid_size[1]-1, iy_max)
        for ix in range(ix_min, ix_max+1):
            for iy in range(iy_min, iy_max+1):
                x = ix * self.resolution
                y = iy * self.resolution
                if (x - cx)**2 + (y - cy)**2 <= r**2:
                    self.occ[ix, iy] = True
        self.circles.append((cx, cy, r))

    def pos_to_idx(self, pos):
        x, y = pos
        ix = int(round(x / self.resolution))
        iy = int(round(y / self.resolution))
        ix = min(max(ix, 0), self.grid_size[0]-1)
        iy = min(max(iy, 0), self.grid_size[1]-1)
        return (ix, iy)

    def idx_to_pos(self, idx):
        ix, iy = idx
        x = ix * self.resolution
        y = iy * self.resolution
        return (x, y)

    def is_occupied_idx(self, idx):
        ix, iy = idx
        return bool(self.occ[ix, iy])

    def is_occupied_pos(self, pos):
        return self.is_occupied_idx(self.pos_to_idx(pos))

def random_obstacles(obs_map, n_rects=5, n_circles=3, max_rect_size=(15,10), max_radius=5):
    """Add random rectangles and circles into the map (attempts to avoid occluding whole map)."""
    w, h = obs_map.grid_size
    for _ in range(n_rects):
        rw = random.randint(2, max_rect_size[0])
        rh = random.randint(2, max_rect_size[1])
        x_min = random.randint(0, max(0, w - rw - 1))
        y_min = random.randint(0, max(0, h - rh - 1))
        x_max = x_min + rw
        y_max = y_min + rh
        obs_map.add_rect((x_min * obs_map.resolution, y_min * obs_map.resolution,
                          x_max * obs_map.resolution, y_max * obs_map.resolution))
    for _ in range(n_circles):
        r = random.randint(2, max_radius)
        cx = random.randint(r, w - r - 1)
        cy = random.randint(r, h - r - 1)
        obs_map.add_circle((cx * obs_map.resolution, cy * obs_map.resolution, r * obs_map.resolution))
