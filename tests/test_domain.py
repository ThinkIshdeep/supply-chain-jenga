import base64, io, json, math, unittest
import numpy as np
from lab.core import astar, clean
from lab import supply

class CoreTests(unittest.TestCase):

    def test_astar_routes_around_wall(self):
        path = astar([0, 0], [4, 4], [[2, y] for y in range(4)], 5)
        self.assertEqual(path[-1], [4, 4])
        self.assertTrue(all((p[0] != 2 or p[1] == 4 for p in path)))

    def test_astar_impossible(self):
        self.assertEqual(astar([0, 0], [2, 2], [[1, y] for y in range(3)], 3), [])

    def test_json_serialization(self):
        self.assertEqual(clean({'a': np.int64(2), 'b': float('nan')}), {'a': 2, 'b': None})

class SupplyTests(unittest.TestCase):

    def test_inventory_nonnegative(self):
        self.assertGreaterEqual(supply.Engine().state['current']['minimum_inventory'], 0)

    def test_replay_determinism(self):
        e = supply.Engine()
        a = e.rollout('fixed', 333)
        b = e.rollout('fixed', 333)
        self.assertEqual(a, b)
