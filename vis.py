#!/usr/bin/env python3

import roblib as rb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(x, y, z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    c = x + y + z
    ax.scatter(x, y, z, c=c)

if __name__ == "__main__":
    pts = rb.array([[0],[0],[0]])

    with open("pts.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            col = np.fromstring(line, dtype=float, sep=' ')
            col = np.array([col]).T
            pts = rb.hstack((pts, col))

    pts = np.vstack((pts, np.ones(pts.shape[1])))

    fig = rb.figure()
    ax = rb.Axes3D(fig)

    rb.draw_axis3D(ax, 0, 0, 0, np.eye(3), 1)
    rb.plot3D(ax, pts, "blue", 2)

    print(pts)
