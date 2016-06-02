import MotorControlGrid as mcg
import time

ss = mcg.MotorControlGrid()

# ss.runMotor_byInterval('x', -.75, 2)
# ss.runMotor_byInterval('y', .01, 2)

ss.runMotorGridPoint(-1, -1, .12)

# time.pause(10)

points = [(1,-1), (-1,-1), (-1,1), (1,1)]
speed = .12
repetitions = 1
# while(True):	#runs infinetly . stopped with python kill shortcut, ctrl+c
while(repetitions > 0):
	for element in points:
		ss.runMotorGridPoint(element[0], element[1], speed)
		
	repetitions = repetitions - 1

raw_input("\nTasks Complete\nPress Return... ")