# run_simulator.py
"""
Multi-drone simulator entrypoint.
- creates random (or manual) obstacles (rectangles & circles)
- creates multiple drones with goals
- computes A* paths per drone
- runs PID controllers with simple inter-drone repulsion
- visualizes everything
"""
from src.planner import AStarPlanner
from src.drone import Drone
from src.obstacles import ObstacleMap, random_obstacles
from src.controller import PIDController
from src.viz import Visualizer
import numpy as np
import random

def main():
    random.seed(1)
    np.random.seed(1)

    grid_size = (80, 50)   # width x height in cells
    resolution = 1.0       # meters per cell

    # create obstacle map
    obs_map = ObstacleMap(grid_size, resolution)

    # Option A: specify obstacles manually (rectangles and circles)
    manual_rects = [
        (10, 5, 16, 22),
        (28, 10, 34, 30),
        (42, 2, 48, 20),
        (60, 35, 72, 45),
    ]
    for r in manual_rects:
        obs_map.add_rect(r)

    manual_circles = [
        (22, 36, 3),   # center_x, center_y, radius
        (50, 12, 4),
    ]
    for c in manual_circles:
        obs_map.add_circle(c)

    # Option B: or add random obstacles (uncomment if desired)
    # random_obstacles(obs_map, n_rects=6, n_circles=4, max_rect_size=(12,10), max_radius=6)

    # define multiple drones (start positions) and goals
    # ensure starts & goals are in free space
    starts = [(2.0, 2.0), (5.0, 8.0), (8.0, 40.0)]
    goals  = [(75.0, 45.0), (72.0, 8.0), (65.0, 28.0)]

    drones = []
    for s in starts:
        drones.append(Drone(x=s[0], y=s[1], yaw=0.0, max_speed=4.0))

    # per-drone planner + compute static paths
    planner = AStarPlanner(obs_map)
    paths = []
    for i, drone in enumerate(drones):
        start = (drone.x, drone.y)
        goal = goals[i]
        path = planner.plan(start, goal)
        if path is None:
            print(f"[Warning] No path for drone {i+1} from {start} -> {goal}")
        paths.append(path)

    # controllers for each drone
    controllers = [PIDController(kp=1.2, ki=0.0, kd=0.25, dt=0.1, max_speed=3.5) for _ in drones]

    # visualizer with multi-drones and paths
    vis = Visualizer(obs_map, starts, goals, paths, drones, save_frames=True)

    dt = 0.1
    max_steps = 4000

    # helper: for each drone track current waypoint index
    path_indices = [0 if p is not None else -1 for p in paths]

    for step in range(max_steps):
        all_reached = True
        # update each drone
        for i, drone in enumerate(drones):
            path = paths[i]
            if path is None:
                continue
            if path_indices[i] >= len(path):
                continue

            all_reached = False
            # target waypoint
            target = path[path_indices[i]]

            # if reached waypoint, advance index
            if np.hypot(drone.x - target[0], drone.y - target[1]) < 0.8:
                path_indices[i] += 1
                # clamp
                if path_indices[i] >= len(path):
                    continue
                target = path[path_indices[i]]

            # compute repulsive vector from other drones (simple)
            other_positions = [(d.x, d.y) for j, d in enumerate(drones) if j != i]

            vx, vy = controllers[i].compute(drone, target, neighbors=other_positions)
            # step drone
            drone.step(vx, vy, dt)

        vis.update(drones, paths, path_indices, step)

        if vis.quit:
            break

        if all_reached:
            print("All drones reached their goals.")
            break

    vis.finish()
    print("Simulation finished.")

if __name__ == "__main__":
    main()
