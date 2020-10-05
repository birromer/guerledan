#!/usr/bin/env python3

import roblib as rb
import numpy as np

fig = rb.figure()
ax = rb.Axes3D(fig)






if __name__ == "__main__":
    with open("pts.csv", "r") as f:
        pts = rb.array([])
        lines = f.readlines()
        for line in lines:
            collumn = np.fromstring(line, dtype=float, sep=' ')
            rb.hstack(pts, collumn)
        print(pts)
