import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle


class Visualizer:
    def __init__(self, obs_map, starts, goals, paths, drones, save_frames=False):
        """
        obs_map: ObstacleMap
        starts: list of (x,y)
        goals: list of (x,y)
        paths: list of lists of (x,y) or None
        drones: list of Drone objects
        """
        self.obs_map = obs_map
        self.starts = starts
        self.goals = goals
        self.paths = paths
        self.drones = drones
        self.quit = False
        self.save_frames = save_frames
        if save_frames:
            os.makedirs("frames", exist_ok=True)
        self.frame_id = 0

        self.fig, self.ax = plt.subplots(figsize=(10,7))
        self.ax.set_xlim(0, obs_map.grid_size[0]*obs_map.resolution)
        self.ax.set_ylim(0, obs_map.grid_size[1]*obs_map.resolution)
        self.ax.set_aspect('equal')

        # draw obstacles (rectangles)
        for (x_min, y_min, x_max, y_max) in obs_map.rects:
            w = x_max - x_min
            h = y_max - y_min
            rect = Rectangle((x_min, y_min), w, h, color='red', alpha=0.6)
            self.ax.add_patch(rect)
        # draw circles
        for (cx, cy, r) in obs_map.circles:
            circ = Circle((cx, cy), r, color='maroon', alpha=0.6)
            self.ax.add_patch(circ)

        # plot starts and goals
        for s in starts:
            self.ax.plot([s[0]],[s[1]], marker='o', markersize=7, color='blue')
        for g in goals:
            self.ax.plot([g[0]],[g[1]], marker='*', markersize=12, color='gold')

        # plot planned paths for each drone
        self.path_lines = []
        colors = ['green','lime','darkorange','magenta','cyan','brown']
        for p, col in zip(paths, colors):
            if p is None:
                self.path_lines.append(None)
                continue
            px = [pt[0] for pt in p]
            py = [pt[1] for pt in p]
            ln, = self.ax.plot(px, py, linestyle='--', linewidth=2, color=col, alpha=0.9)
            self.path_lines.append(ln)

        # create drone markers
        self.drone_points = []
        drone_colors = ['cyan','magenta','orange','green','purple','navy']
        for i, drone in enumerate(drones):
            dp, = self.ax.plot([], [], marker='o', markersize=8, color=drone_colors[i % len(drone_colors)], label=f'drone_{i+1}')
            self.drone_points.append(dp)

        self.ax.legend()
        plt.ion()
        plt.show()

    def update(self, drones, paths, path_indices, step):
        # update drone positions and histories
        for i, drone in enumerate(drones):
            self.drone_points[i].set_data([drone.x], [drone.y])
            # draw history
            if len(drone.history) > 1:
                hx = [p[0] for p in drone.history]
                hy = [p[1] for p in drone.history]
                self.ax.plot(hx, hy, linewidth=1, alpha=0.5)
            # optionally update current target on path
            # update path line alpha to show progress
            ln = self.path_lines[i] if i < len(self.path_lines) else None
            if ln is not None and path_indices and path_indices[i] >= 0:
                # fade the portion already passed by updating segments is complex;
                # keep static path for clarity
                pass

        plt.pause(0.001)
        if self.save_frames:
            fname = f"frames/frame_{self.frame_id:04d}.png"
            self.fig.savefig(fname)
            self.frame_id += 1
        if not plt.fignum_exists(self.fig.number):
            self.quit = True

    def finish(self):
        plt.ioff()
        plt.show()
