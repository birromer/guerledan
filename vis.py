#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot(ax, x, y, z):
    c = x + y + z
    ax.scatter(x, y, z, c=c)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    plt.show()

def get_center(pts):
    max_x = max(pts[0,:])
    min_x = min(pts[0,:])
    max_y = max(pts[1,:])
    min_y = min(pts[1,:])
    max_z = max(pts[2,:])
    min_z = min(pts[2,:])

    c_x = (min_x + max_x)/2
    c_y = (min_y + max_y)/2
    c_z = (min_z + max_z)/2

    return c_x, c_y, c_z


def get_transl_m(x,y,z):
    T = np.eye(4)
    T[0,3] = -x
    T[1,3] = -y
    T[2,3] = -z
    print(T)

    return T


def opt(pts):
    P0 = np.array([[0], [0], [0], [1], [1], [1], [0], [0], [0]])
    print(P0.T.shape)


if __name__ == "__main__":
    pts = np.array([[0],[0],[0]])
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    with open("pts.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            col = np.fromstring(line, dtype=float, sep=' ')
            col = np.array([col]).T
            pts = np.hstack((pts, col))

    pts = np.vstack((pts, np.ones(pts.shape[1])))
    pts = np.delete(pts, 0, 1)
    print(pts)

    cx, cy, cz = get_center(pts)
    print("cx:", cx, "cy:", cy, "cz:", cz)

    T = get_transl_m(cx,cy,cz)

    pts = T @ pts

    opt(pts)

#    plot(ax, pts[0,:], pts[1,:], pts[2,:])
