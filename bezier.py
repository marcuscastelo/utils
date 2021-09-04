# Props to Mikhail M. and azazelspeaks for the original code.
# https://stackoverflow.com/questions/44467329/pyautogui-mouse-movement-with-bezier-curve

import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
import math

def point_dist(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def move_bezier(xDest, yDest, moveDuration = 0.1):
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    x1, y1 = pyautogui.position()  # Starting position

    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, xDest, num=cp, dtype='int')
    y = np.linspace(y1, yDest, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    RND = 20
    xr = [random.randint(-RND, RND) for k in range(cp)]
    yr = [random.randint(-RND, RND) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
                                    # Must be less than number of control points.
    tck, u = interpolate.splprep([x, y], k=degree)
    # Move upto a certain number of points
    u = np.linspace(0, 1, num=2+int(point_dist(x1,y1,xDest,yDest)/50.0))
    points = interpolate.splev(u, tck)

    # Move mouse.
    timeout = moveDuration / len(points[0])
    point_list=zip(*(i.astype(int) for i in points))
    for point in point_list:
        pyautogui.moveTo(*point)
        time.sleep(timeout)
