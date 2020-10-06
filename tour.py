#!/usr/bin/env python3

import roblib as rb


def f(x,u):
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    x1dot = x4 * rb.cos(x3)
    x2dot = x4 * rb.sin(x3)
    x3dot = p1 * (u1 - u2)
    x4dot = p2 * (u1 + u2) - p3 * abs(x4) * x4


def sim():
    dt = 0.01
    x = rb.array([
        [0],
        [0],
        [0],
        [0.1]
    ])


    for t in rb.arange(0,10,dt):
        u = 0
        x = x + dt*f(x,u)



if __name__ == "__main__":
    psibar = 0
