#Scans the stage in the y DIRECTION ONLY because spacing is equal to 0.0

import MotorControlGrid as mcg
import numpy as np
import time

motorNames = ['x', 'y']
ss = mcg.MotorControlGrid(motorNames)

#start deposition off of substrate and pan onto it
apertureW = 0.1
apertureH = 0.1
passes = 2
spacing = 0.0
scanDistance = 1.5
intervals = [7,7] #Have to give as many intervals as there are passes
maxSpeed = 0.254

#starts off in positive y direction and always moves positive x
len = -scanDistance
for i in range(passes):
	len = -len #makes it so y changes back and forth from positive to negative direction
	ss.runMotor_byInterval(motorNames[1], len, intervals[i]) #run y scanDistance length
	ss.waitInterupt(motorNames[1]) #wait for y to finish running
	ss.waitInterupt(motorNames[0])
	# ss.runMotor(motorNames[0], spacing, maxSpeed)
	# ss.waitInterupt(motorNames[1])
	# ss.waitInterupt(motorNames[0]) #wait for x to finish running
	
raw_input("\n\nPress Return...\n\n")