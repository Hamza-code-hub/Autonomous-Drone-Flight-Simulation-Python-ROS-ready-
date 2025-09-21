import heapq
import math

class AStarPlanner:
    def __init__(self, obstacle_map):
        self.map = obstacle_map
        self.width, self.height = obstacle_map.grid_size

    def plan(self, start, goal):
        start_idx = self.map.pos_to_idx(start)
        goal_idx  = self.map.pos_to_idx(goal)
        if self.map.is_occupied_idx(goal_idx):
            print("Goal inside obstacle!")
            return None

        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start_idx, goal_idx), 0, start_idx, None))
        came_from = {}
        cost_so_far = {start_idx: 0}

        while open_set:
            _, g, current, parent = heapq.heappop(open_set)
            if current in came_from:
                continue
            came_from[current] = parent
            if current == goal_idx:
                return self.reconstruct_path(came_from, current)

            for n in self.get_neighbors(current):
                if self.map.is_occupied_idx(n):
                    continue
                new_cost = cost_so_far[current] + self.dist(current, n)
                if n not in cost_so_far or new_cost < cost_so_far[n]:
                    cost_so_far[n] = new_cost
                    priority = new_cost + self.heuristic(n, goal_idx)
                    heapq.heappush(open_set, (priority, new_cost, n, current))
        return None

    def reconstruct_path(self, came_from, current):
        path_idx = []
        while current is not None:
            path_idx.append(current)
            current = came_from[current]
        path_idx.reverse()
        return [self.map.idx_to_pos(idx) for idx in path_idx]

    def get_neighbors(self, idx):
        x, y = idx
        neighbor_offsets = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1)]
        res = []
        for dx, dy in neighbor_offsets:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                res.append((nx, ny))
        return res

    def heuristic(self, a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])

    def dist(self, a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])
