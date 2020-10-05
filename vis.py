#!/usr/bin/env python3

import roblib as rb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(ax, x, y, z):
    c = x + y + z
    ax.scatter(x, y, z, c=c)

if __name__ == "__main__":
    pts = rb.array([[0],[0],[0]])
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    with open("pts.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            col = np.fromstring(line, dtype=float, sep=' ')
            col = np.array([col]).T
            pts = rb.hstack((pts, col))

    pts = np.vstack((pts, np.ones(pts.shape[1])))

    plot(ax, pts[0,:], pts[1,:], pts[2,:])

    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")

    plt.show()
