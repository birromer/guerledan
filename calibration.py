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


def get_center_and_len(pts):
    max_x = max(pts[0,:])
    min_x = min(pts[0,:])
    max_y = max(pts[1,:])
    min_y = min(pts[1,:])
    max_z = max(pts[2,:])
    min_z = min(pts[2,:])

    c_x = (min_x + max_x)/2
    c_y = (min_y + max_y)/2
    c_z = (min_z + max_z)/2

    l_x = (max_x - min_x)
    l_y = (max_y - min_y)
    l_z = (max_z - min_z)

    return c_x, c_y, c_z, l_x, l_y, l_z


def get_transl_m(x,y,z):
    T = np.eye(4)
    T[0,3] = -x
    T[1,3] = -y
    T[2,3] = -z
    print(T)

    return T


def opt(x, pts, p):
    p4, p5, p6 = p[3], p[4], p[5]
    p1, p2, p3 = p[0], p[1], p[2]

    fp_1 = np.array([
        [p4, 0, 0],
        [0, p5, 0],
        [0, 0, p6]
    ], dtype=float)

    fp_2 = np.array([
        pts[0,:] - p1,
        pts[1,:] - p2,   # mudar pq iss ja deveria ser a aplicação direta nos pontos, nao estou gerando uma matriz itermediaria
        pts[2,:] - p3
    ], dtype=float)

    return fp_1 @ fp_2


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

#    pts = np.vstack((pts, np.ones(pts.shape[1])))
    pts = np.delete(pts, 0, 1)
    print(pts)

    cx, cy, cz, lx, ly, lz = get_center_and_len(pts)
    print("cx:", cx, "cy:", cy, "cz:", cz)
    print("lx:", lx, "ly:", ly, "lz:", lz)

    p = np.array([
        [cx],
        [cy],
        [cz],
        [lx],
        [ly],
        [lz]
    ])

    T = get_transl_m(cx,cy,cz)

    opt_m = opt([0,0,0], pts, p)
#    print(opt_m.shape)
#    print(pts.shape)

#    pts = opt_m.T @ pts
    pts =T @ pts

#    print(pts.shape)

    plot(ax, pts[0,:], pts[1,:], pts[2,:])