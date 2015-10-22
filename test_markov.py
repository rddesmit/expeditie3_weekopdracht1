from markov import Markov
from orientation import Orientation
from colors import Colors
import time
import unittest


class TestMarkov(unittest.TestCase):

    def test_normalize(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_normalize", 1, 0, 0)
        markov.normalize()

        total = reduce(lambda acc, c: acc + sum(c), markov._p, 0.)
        self.assertTrue(total == 1)

    def test_update(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_update", 1, 0, 0)
        markov.update(1)

        p = [[1., 0., 0.]]
        self.assertListEqual(markov._p, p)

    def test_normalize_after_update(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_normalize_after_update", 1, 0, 0)
        markov.update(1)

        total = reduce(lambda acc, c: acc + sum(c), markov._p, 0.)
        self.assertTrue(total == 1)

    def test_move_north(self):
        map = [[1, 2, 3],
               [2, 3, 3],
               [3, 2, 3]]
        markov = Markov(map, Orientation.NORTH, "test_move_north", 1, 0, 0)
        markov.update(1)
        markov.move(1)

        p = [[0., 0., 0.],
             [0., 0., 0.],
             [1., 0., 0.]]
        self.assertListEqual(markov._p, p)

    def test_move_east(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_move_east", 1, 0, 0)
        markov.update(1)
        markov.move(1)

        p = [[0., 1., 0.]]
        self.assertListEqual(markov._p, p)

    def test_move_south(self):
        map = [[1, 2, 3],
               [2, 3, 3],
               [3, 2, 3]]
        markov = Markov(map, Orientation.SOUTH, "test_move_south", 1, 0, 0)
        markov.update(1)
        markov.move(1)

        p = [[0., 0., 0.],
             [1., 0., 0.],
             [0., 0., 0.]]
        self.assertListEqual(markov._p, p)

    def test_move_west(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.WEST, "test_move_west", 1, 0, 0)
        markov.update(1)
        markov.move(1)

        p = [[0., 0., 1.]]
        self.assertListEqual(markov._p, p)

    def test_p_hit(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_p_hit", .75, 0, 0)
        markov.update(1)

        p = [[.6, .2, .2]]
        self.assertAlmostEqual(markov._p[0][0], p[0][0])
        self.assertAlmostEqual(markov._p[0][1], p[0][1])
        self.assertAlmostEqual(markov._p[0][2], p[0][2])

    def test_p_overshoot(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_p_overshoot", 1, .5, 0)
        markov.update(1)
        markov.move(1)

        p = [[0., .5, .5]]
        self.assertListEqual(markov._p, p)

    def test_p_undershoot(self):
        map = [[1, 2, 3]]
        markov = Markov(map, Orientation.EAST, "test_p_undershoot", 1, 0, .5)
        markov.update(1)
        markov.move(1)

        p = [[.5, .5, 0.]]
        self.assertListEqual(markov._p, p)


