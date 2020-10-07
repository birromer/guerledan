#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate


def plot_mesh(ax, pts):
    nx = ny = len(ax)
    x = np.linspace(0, nx-1, ny)
    y = np.linspace(0, ny-1, nx)
    X,Y = np.meshgrid(pts[0,:], pts[1,:], indexing='xy')


def plot_scatter(ax, x, y, z):
    c = x + y + z
    ax.scatter(x, y, z, c=c)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    plt.show()

if __name__ == "__main__":
    pts = np.array([[0],[0],[0]])
    fig = plt.figure()
#    ax = plt.axes(projection='3d')

    with open("data/acc.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            col = np.fromstring(line, dtype=float, sep=' ')
            col = np.array([col]).T
            pts = np.hstack((pts, col))
    pts = np.delete(pts, 0, 1)

#    plot_scatter(ax, pts[0,:], pts[1,:], pts[2,:])

    ft1 = np.fft.fft(pts[0,:])
    ft2 = np.fft.fft(pts[1,:])


    copy_x = pts[0,:].copy()
    copy_y = pts[1,:].copy()
    print(copy_x)

    print(copy_x.sort())
    print(copy_y.sort())

    base = np.arange(0,pts.shape[1])
#    plt.plot(base, ft2, label="Y axis acc")
#    plt.plot(base, ft1, label="X axis acc")

    plt.plot(base, pts[0,:], label="X axis acc")
    plt.plot(base, pts[1,:], label="Y axis acc")
#    plt.plot(base, pts[2,:], label="Z axis acc")

    plt.xlabel('axis')
    plt.ylabel('freq')
    plt.legend()
    plt.show()
