#!/usr/bin/env python3

import roblib as rb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = rb.figure()
ax = rb.Axes3D(fig)

def plot(x, y, z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    c = x + y + z
    ax.scatter(x, y, z, c=c)

if __name__ == "__main__":
    with open("pts.csv", "r") as f:
        pts = rb.array([])
        lines = f.readlines()
        for line in lines:
            collumn = np.fromstring(line, dtype=float, sep=' ')
            rb.hstack(pts, collumn)
        print(pts)
