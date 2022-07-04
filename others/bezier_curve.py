import time
import math
from scipy.interpolate import BPoly
import numpy as np
import matplotlib.pyplot as plt
import random


# Start element info
s_location = start.location
x, y = s_location['x'], s_location['y']
s_size = start.size
w, h = s_size['width'], s_size['height']
wCenter = w/2
hCenter = h/2
pStart = [int(wCenter + x), int(hCenter + y)]

# pStart = {'x':146, 'y':3952}
# pEnd = {'x':291, 'y':3952}
#s_size = start.size

# End element info
# e_location = end.location
# x, y = e_location['x'], e_location['y']
# e_size = start.size
# w, h = e_size['width'], e_size['height']
# wCenter = w/2
# hCenter = h/2
# p4 = [int(wCenter + x), int(hCenter + y)]


p1 = [0,0]
p4 = [
pEnd['x'] - pStart['x'],
pEnd['y'] - pStart['y']
]
#e_size = end.size

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
x_coordinates = np.linspace(0,1,50)
coordinates = curve(x_coordinates)
print(coordinates)

# for x, y in coordinates:
#     action.move_to_location(x, y)
#     action.perform()
#     time.sleep(0.03)

# Plot bezier curve
plt.plot(*coordinates.T)
plt.show()


