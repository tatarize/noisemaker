from __future__ import print_function

import random
import unittest

import numpy as np

from noisemaker import *


class TestNoise(unittest.TestCase):

    def test_regular_movement(self):
        ax = random.randint(-100, 100)
        ay = random.randint(-100, 100)

        j = noise((1, 100), (ax, ay))
        k = noise((1, 100), (ax, ay + 1))  # K is moved down by 1.
        q = j[0, 1:100] - k[0, 0:99]  # move was in the y direction.
        self.assertFalse(np.any(q))

        j = noise((100, 1), (ax, ay))
        k = noise((100, 1), (ax + 1, ay))  # K is moved right by 1.
        q = j[1:100, 0] - k[0:99, 0]  # move was in the x direction
        self.assertFalse(np.any(q))

    def test_deterministic_slices(self):
        n = 20
        while True:
            ox = random.randint(-10000, 10000)
            oy = random.randint(-10000, 10000)
            ax = random.randint(-100, 100)
            ay = random.randint(-100, 100)
            aw = random.randint(0, 100)
            ah = random.randint(0, 100)
            bx = random.randint(-100, 100)
            by = random.randint(-100, 100)
            bw = random.randint(0, 100)
            bh = random.randint(0, 100)

            x0 = max(ax, bx)
            y0 = max(ay, by)
            x1 = min(ax + aw, bx + bw)
            y1 = min(ay + ah, by + bh)

            if x0 < x1 and y0 < y1:
                # Only overlapped bounds count as a test.
                a = noise((aw, ah), (ax + ox, ay + oy))
                b = noise((bw, bh), (bx + ox, by + oy))
                axr = slice(x0 - ax, x1 - ax)
                ayr = slice(y0 - ay, y1 - ay)
                bxr = slice(x0 - bx, x1 - bx)
                byr = slice(y0 - by, y1 - by)
                a_part = a[axr, ayr]
                b_part = b[bxr, byr]
                q = a_part - b_part
                self.assertFalse(np.any(q))
                n -= 1
                if n <= 0:
                    break

    def test_deterministic_gaussian_slices(self):
        n = 20
        while True:
            ox = random.randint(-10000, 10000)
            oy = random.randint(-10000, 10000)
            ax = random.randint(-100, 100)
            ay = random.randint(-100, 100)
            aw = random.randint(0, 100)
            ah = random.randint(0, 100)
            bx = random.randint(-100, 100)
            by = random.randint(-100, 100)
            bw = random.randint(0, 100)
            bh = random.randint(0, 100)

            x0 = max(ax, bx)
            y0 = max(ay, by)
            x1 = min(ax + aw, bx + bw)
            y1 = min(ay + ah, by + bh)

            if x0 < x1 and y0 < y1:
                # Only overlapped bounds count as a test.
                a = noise((aw, ah), (ax + ox, ay + oy), kernel=GAUSSIAN)
                b = noise((bw, bh), (bx + ox, by + oy), kernel=GAUSSIAN)
                axr = slice(x0 - ax, x1 - ax)
                ayr = slice(y0 - ay, y1 - ay)
                bxr = slice(x0 - bx, x1 - bx)
                byr = slice(y0 - by, y1 - by)
                a_part = a[axr, ayr]
                b_part = b[bxr, byr]
                q = a_part - b_part
                self.assertFalse(np.any(q))
                n -= 1
                if n <= 0:
                    break
