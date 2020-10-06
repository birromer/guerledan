#!/usr/bin/env python3

import roblib as rb
from north import norm


def g(x):
    return rb.arctan2(x[1], x[0])  # psi

def f(x,u):
    p1, p2, p3 = 0.1, 0.2, 0.1  # calibrate later

    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    u1, u2 = u[0], u[1]

    x1dot = x4 * rb.cos(x3)
    x2dot = x4 * rb.sin(x3)
    x3dot = p1 * (u1 - u2)
    x4dot = p2 * (u1 + u2) - p3 * abs(x4) * x4

    return rb.array([
        x1dot,
        x2dot,
        x3dot,
        x4dot,
    ])


if __name__ == "__main__":
    ax = rb.init_figure(-30,30, -30,30)

    psibar = 0
    dt = 0.01
    x = rb.array([
        [3],        # x
        [9],        # y
        [10.4],     # heading
        [100.1]     # speed
    ])

    for t in rb.arange(0,1,dt):
        rb.clear(ax)
#        psi = rb.arctan2(x[1], x[2])
        psi = x[2]

        error = rb.sawtooth(psi - psibar)
        print("error = ", error)
        error_norm = norm(error)

        print(error_norm*50)

        u = rb.array([
            [1],
            [1]
#            50 * error_norm,
#            50 * (1 - error_norm)
        ])

        x = x + dt*f(x, u)
        print("x:", x)
        print("t:", t)

        rb.draw_tank(x, 'red')
