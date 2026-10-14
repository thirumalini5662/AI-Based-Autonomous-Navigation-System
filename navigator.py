class Navigator:
    # Simple waypoint-following controller for the virtual agent.
    def __init__(self, path):
        self.path = path
        self.index = 0

    @property
    def position(self):
        return self.path[min(self.index, len(self.path)-1)] if self.path else None

    @property
    def finished(self):
        return bool(self.path) and self.index >= len(self.path)-1

    def step(self):
        if self.path and not self.finished:
            self.index += 1
        return self.position

    def progress(self):
        if len(self.path) <= 1:
            return 100.0
        return self.index / (len(self.path)-1) * 100

    def distance_remaining(self):
        if not self.path:
            return 0
        return max(0, len(self.path)-1-self.index)
