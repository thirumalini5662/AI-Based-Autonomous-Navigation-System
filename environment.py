import numpy as np


class GridEnvironment:
    # 0 = free cell, 1 = obstacle.
    def __init__(self, width, height, obstacle_density=0.18, seed=42,
                 start=(1, 1), goal=(28, 18)):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.grid = self._create_map(obstacle_density, seed)

    def _create_map(self, density, seed):
        rng = np.random.default_rng(seed)
        grid = (rng.random((self.height, self.width)) < density).astype(np.uint8)
        sx, sy = self.start
        gx, gy = self.goal
        grid[sy, sx] = 0
        grid[gy, gx] = 0

        # Keep a guaranteed open corridor so the demo remains reliable.
        grid[sy, :] = 0
        grid[:, self.width - 2:] = 0
        return grid

    def is_free(self, position):
        x, y = position
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.grid[y, x] == 0

    def neighbors(self, position):
        x, y = position
        candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        return [p for p in candidates if self.is_free(p)]
