#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


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

def opt(pt, p):
    p1, p2, p3 = p[0], p[1], p[2]
    p4, p5, p6 = p[3], p[4], p[5]
    x, y, z = pt[0], pt[1], pt[2]

    fp_1 = np.array([
        [p4, 0, 0],
        [0, p5, 0],
        [0, 0, p6]
    ], dtype=float)

    fp_2 = np.array([
        x - p1,
        y - p2,
        z - p3
    ], dtype=float)

    return np.matmul(fp_1, fp_2)


def opt2(pt, x1, xm1, x2, x3):
    A = np.zeros((3,3))
    xv = np.array([x1,x2,x3])
    beta = 46000

    b = -(x1 + xm1)/2

    for i in range(len(pt[0,:])):
        pt[0,i] = pt[0,i] + b[0]

    for i in range(len(pt[1,:])):
        pt[1,i] = pt[1,i] + b[1]

    for i in range(len(pt[2,:])):
        pt[2,i] = pt[2,i] + b[2]

    A[:,0] = (x1 + b)/beta
    A[:,1] = (x2 + b)/beta
    A[:,2] = (x3 + b)/beta

    opt_pt = np.matmul(np.linalg.inv(A), pt)

    return opt_pt


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

    pts = np.delete(pts, 0, 1)

    cx, cy, cz, lx, ly, lz = get_center_and_len(pts)
    print("cx:", cx, "cy:", cy, "cz:", cz)
    print("lx:", lx, "ly:", ly, "lz:", lz)

#    p = np.array([
#        [cx],
#        [cy],
#        [cz],
#        [lx],
#        [ly],
#        [lz]
#    ])
#    T = get_transl_m(cx,cy,cz)
#    opt_pts1 = opt(pts, p)
#    opt_pts1 = np.vstack((opt_pts1, np.ones(pts.shape[1])))
#    opt_pts1 = np.matmul(T, opt_pts1)
#    plot(ax, opt_pts1[0,:], opt_pts1[1,:], opt_pts1[2,:])

    x1 = np.array([900, -3950, 5540])
    xm1 = np.array([7050, -2950, 5400])
    x2 = np.array([4410, -6400, 5450])
    x3 = np.array([3950, -3450, 2300])

    opt_pts2 = opt2(pts, x1, xm1, x2, x3)
    plot(ax, opt_pts2[0,:], opt_pts2[1,:], opt_pts2[2,:])
