import unittest
from src.environment import GridEnvironment
from src.planner import astar


class TestAStar(unittest.TestCase):
    def test_path_exists_on_open_grid(self):
        env = GridEnvironment(8, 8, 0.0, 1, (0, 0), (7, 7))
        path, expanded = astar(env, (0, 0), (7, 7))
        self.assertTrue(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (7, 7))
        self.assertGreater(expanded, 0)

    def test_path_avoids_obstacles(self):
        env = GridEnvironment(10, 10, 0.1, 3, (0, 0), (9, 9))
        path, _ = astar(env, (0, 0), (9, 9))
        for point in path:
            self.assertTrue(env.is_free(point))


if __name__ == "__main__":
    unittest.main()
