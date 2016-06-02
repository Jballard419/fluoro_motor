import MotorControlGrid as mcg
import numpy as np

ss = mcg.MotorControlGrid()

# circle
radius = 1
increment = .1
length = 2 * np.pi * radius

t = np.arange(0, length, increment)
x = radius * np.sin(t)
y = radius * np.cos(t)

# x = [-.5, .5, 0]
# y = [.5, -.5, 0]

ss.runMotorGridCurve(x, y, 0.254)

ss.runMotorGridPoint(0, 0, 0.254)