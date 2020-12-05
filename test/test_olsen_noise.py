from __future__ import print_function

import random
import unittest

import numpy as np

from OlsenNoise import noise


class TestNoise(unittest.TestCase):

    def test_deterministic_noise(self):
        c = noise(0, 0, 102, 102)
        d = noise(1, 1, 100, 100)
        q = c[1:91, 1:91] - d[0:90, 0:90]
        if np.any(q):
            print(q)
        self.assertFalse(np.any(q))

        c = noise(0, 0, 102, 102)
        d = noise(5, 5, 100, 100)
        q = c[5:95, 5:95] - d[0:90, 0:90]
        if np.any(q):
            print(q)
        self.assertFalse(np.any(q))

        c = noise(0, 0, 102, 102)
        d = noise(10, 10, 102, 102)
        q = c[10:60, 10:60] - d[0:50, 0:50]
        if np.any(q):
            print(q)
        self.assertFalse(np.any(q))

        c = noise(50, 50, 102, 102)
        d = noise(60, 60, 102, 102)
        q = c[10:60, 10:60] - d[0:50, 0:50]
        if np.any(q):
            print(q)
        self.assertFalse(np.any(q))

    def test_position_shift_x(self):
        for dx in range(30):
            a = noise(50, 50, 102, 102)
            b = noise(50 + dx, 50, 102, 102)
            q = a[dx:50+dx, :50] - b[0:50, 0:50]
            if np.any(q):
                print(q, dx)
            self.assertFalse(np.any(q))

    def test_position_shift_y(self):
        for dy in range(30):
            a = noise(50, 50, 102, 102)
            b = noise(50, 50 + dy, 102, 102)
            q = a[:50, dy:50+dy] - b[0:50, 0:50]
            if np.any(q):
                print(q, dy)
            self.assertFalse(np.any(q))

    def test_position_shift_angle(self):
        for delta in range(50):
            a = noise(50, 50, 102, 102)
            b = noise(50 + delta, 50 + delta, 102, 102)
            q = a[delta:50+delta, delta:50+delta] - b[0:50, 0:50]
            if np.any(q):
                print(q, delta)
            self.assertFalse(np.any(q))

    def test_deterministic_nature(self):
        n = 3
        while True:
            ax = random.randint(-1000, 1000)
            ay = random.randint(-1000, 1000)
            aw = random.randint(0, 1000)
            ah = random.randint(0, 1000)
            bx = random.randint(-1000, 1000)
            by = random.randint(-1000, 1000)
            bw = random.randint(0, 1000)
            bh = random.randint(0, 1000)

            x0 = max(ax, bx)
            y0 = max(ay, by)
            x1 = min(ax + aw, bx + bw)
            y1 = min(ay + ah, by + bh)

            if x0 < x1 and y0 < y1:
                a = noise(ax, ay, aw, ah)
                b = noise(bx, by, bw, bh)
                axr = slice(x0 - ax, x1 - ax)
                ayr = slice(y0 - ay, y1 - ay)
                bxr = slice(x0 - bx, x1 - bx)
                byr = slice(y0 - by, y1 - by)
                a_part = a[axr, ayr]
                b_part = b[bxr, byr]
                q = a_part - b_part
                if np.any(q):
                    print(q)
                self.assertFalse(np.any(q))
                n -= 1
                if n <= 0:
                    break
