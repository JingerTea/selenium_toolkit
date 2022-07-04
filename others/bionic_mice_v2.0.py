import time
import math
from selenium.webdriver.common.action_chains import ActionChains
from scipy.interpolate import BPoly
import numpy as np
import matplotlib.pyplot as plt
import random

def move(action, start, end):
    # Initialize
    action.move_to_element(start)
    time.sleep(1)

    # Start element info
    s_location = start.location
    print(s_location)
    x, y = s_location['x'], s_location['y']
    s_size = start.size
    w, h = s_size['width'], s_size['height']
    wCenter = w/2
    hCenter = h/2
    pStart = {
        'x': int(wCenter + x),
        'y': int(hCenter + y)
    }
    print(pStart)

    # pStart = {'x':146, 'y':3952}
    # pEnd = {'x':291, 'y':3952}
    #s_size = start.size

    # End element info
    e_location = end.location
    print(e_location)
    x, y = e_location['x'], e_location['y']
    e_size = end.size
    w, h = e_size['width'], e_size['height']
    wCenter = w/2
    hCenter = h/2
    pEnd = {
        'x': int(wCenter + x),
        'y': int(hCenter + y)
    }
    print(pEnd)

    p1 = [0,0]
    p4 = [
    pEnd['x'] - pStart['x'],
    pEnd['y'] - pStart['y']
    ]

    # Calculate distance
    distance = int(math.dist(p1, p4)/4)
    print(distance)
    d1 = random.randrange(distance)
    d2 = random.randrange(distance)

    # Generate random points
    p2 = [p1[0]+d1 ,p1[1]+d1]
    p3 = [p4[0]-d2 ,p4[1]-d2]

    # Control points
    cp = [p1, p2, p3, p4]
    cp = np.array(cp)

    # Make bezier curve
    curve = BPoly(cp[:, None, :], [0,1])

    # Creating numeric sequences of bezier curve
    x_coordinates = np.linspace(0,1,20)
    coordinates = curve(x_coordinates)
    print(coordinates)

    # Plot bezier curve
    plt.plot(*coordinates.T)
    plt.show()

    for x, y in coordinates:
        action.move_by_offset(x, y)
        action.perform()
        time.sleep(0.01)




