#Class used to control motors on scanning stage with stepperbee
#Jake Meeth - 2013 08 05

#make motor acceleration more robust (it has bugs I think)
#	first, what if negative speeds are give
# second can I make the second runMotor function and the original into one

import ctypes as ct
import numpy as np
import math
import time
from collections import defaultdict, OrderedDict
import MotorControlConstants as MCC #user defined

class MotorControl:
	"""

	"""
	def __init__(self,  stepMode = 1, inInches = False, interupt = False):
		"""
		__init__(motorNames = ['x', 'y'], stepMode = 1, inches = False)

		inititializes stepperbee

		Parameters
		-------
		motorNames : list of string names assigned to motor 1 and 2 respectively
		stepMode : 0 for wavestep, 1 for full step, 2 for power off
		inches : True to set default values to inches, False for cm
		interupt : True to set runMotor functions to wait for others to finish

		Returns
		-------
		None
		"""





		#hold bool telling if values are in inches or cm
		self.inInches = inInches

		#hold bool telling interupt or not
		self.interupt = interupt

		#check that stepMode is proper value
		if( (stepMode < 0) or (stepMode > 2) ):
			print("ERROR in '__init__(self, stepMode, inInches = False)'\n" +
						"stepMode must be an integer from 0 to 2\n")

		#get reference to stepperbee library
		self.stpLib = ct.WinDLL('stp.dll')

		#initialize and set the stepping mode
		self.status = self.stpLib.InitStp()
		self.stpLib.SetStepMode(stepMode, stepMode)

		#Inform user of status
		print("Stepperbee connection status: " + str(self.status) + " devices connected")

	def runMotor_raw(self, motorName, steps, interval, interupt):
		"""
		runMotor_raw(motorName, steps, interval)

		moves motor steps at interval

		Parameters
		-------
		motorName : string corresponding to name of motor 1 or 2 givin to init
		steps : steps for stepper motor to make
		interval : interval for motor to run at

		Returns
		-------
		None
		"""
		#find motorNum
		motorNum = motorName - 1 #motor num is either 0 or 1
		if(motorNum > 1 and motorNum < 0):

			print("ERROR in 'runMotor_raw(self, motorName, steps, interval)'\n" +
						"motorName not a valid motor\n")
			return

		#find direction for motor to run based on sign of steps
		#it is different for each motor
		direction = 0 #direction is either 0 or 1
		if( steps < 0 and motorNum == 1):
			#direction must be negative
			direction = 1
		elif(steps > 0 and motorNum == 0):
			#direction must be positive
			direction = 1

		steps = abs(steps)

		#set outputs
		outputs = 0

		#run motor
		if(motorNum == 0):
			#check for motor interupt
			if(interupt):
				self.stpLib.RunMotor1(steps, interval, direction, outputs)
			else:
				self.waitInterupt(self.motorNames[0])
				self.stpLib.RunMotor1(steps, interval, direction, outputs)

		else: #motorNum must be 1
			#check for motor interupt
			if(interupt):
				self.stpLib.RunMotor2(steps, interval, direction, outputs)
			else:
				self.waitInterupt(self.motorNames[1])
				self.stpLib.RunMotor2(steps, interval, direction, outputs)






	# def runMotor_byInterval(self, motorName, disp, interval):
	# 	"""
	# 	runMotor(motorName, disp, interval)
	#
	# 	moves motor disp(cm or in) at interval(ms)
	#
	# 	Parameters
	# 	-------
	# 	motorName : string corresponding to name of motor 1 or 2 givin to init
	# 	disp : float specifying the distance for stage to move
	# 	interval : int specifying the speed for stage to move at (max speed = 0.254 cm/s at 1 ms interval)
	#
	# 	Returns
	# 	-------
	# 	steps : number of steps needed to move linear disp
	# 	"""
	# 	steps = self.dispToSteps(disp)
	#
	# 	#make sure direction is preserved
	# 	if(disp < 0):
	# 		steps = steps * -1
	#
	# 	#check that interval isnt negative
	# 	if(interval < 0):
	# 		print("ERROR in 'runMotor_byInterval(self, motorName, disp, interval)'\n" +
	# 					"interval cannot be negative\n")
	# 		return(None)
	#
	# 	#run motor
	# 	self.runMotor_raw(motorName, steps, interval, self.interupt)
	#
	# 	return steps
	#
	# def runMotorAcc(self, motorName, disp, startSpeed, endSpeed):
	# 	"""
	#
	# 	Pros: mostly accuate speeds
	# 	Cons: pause between each speed change. Resolution of speeds is poor
	# 	"""
	# 	#find starting and ending intervals
	# 	startInterval = self.speedToInterval(startSpeed)
	# 	endInterval = self.speedToInterval(endSpeed)
	#
	# 	#find number of steps required
	# 	stepCount = self.dispToSteps(abs(disp))
	#
	# 	#generate array of all intervals it must go through to be as uniform as possible
	# 	#generate an equally spaced list of floats from start to finish
	# 	accProfile = np.linspace(startInterval, endInterval, abs(stepCount))
	#
	# 	#convert each float to int (since interval ms must be int)
	# 	accProfile = [ int(element) for element in accProfile]
	#
	# 	#count each occurence of each int in the profile
	# 	#this way we can tell the motor to run 3 steps at an interval instead of 1 step at an interval
	# 	#	and then again and again a third time
	# 	summary = defaultdict(int)
	# 	for i in accProfile:
	# 		summary[i] += 1
	#
	# 	summaryItems = summary.items()
	# 	if(startSpeed > endSpeed):
	# 		summaryItems.reverse()
	#
	# 	summary = OrderedDict(summaryItems)
	#
	# 	#send each runMotor command consecutively
	# 	r = len(summary)
	# 	for i in range(r):
	# 		task = summary.popitem() #task = (interval, steps)
	#
	# 		#preserve direction
	# 		if(disp < 0):
	# 			self.runMotor_raw(motorName, -1 * task[1], task[0], False)
	# 		else:
	# 			self.runMotor_raw(motorName, task[1], task[0], False)
	#
	# def runMotorAcc_stepByStep(self, motorName, disp, startSpeed, endSpeed, resolution = 25):
	# 	"""
	#
	# 	Pros: precise (not accurate) at slow speed
	# 	Cons:very slow and not accurate speed input
	# 	"""
	# 	#find starting and ending intervals
	# 	startInterval = self.speedToInterval(startSpeed)
	# 	endInterval = self.speedToInterval(endSpeed)
	#
	# 	#find number of steps required
	# 	stepCount = self.dispToSteps(abs(disp))
	#
	# 	#generate array of all intervals it must go through to be as uniform as possible
	# 	#generate an equally spaced list of floats from start to finish
	# 	accProfile = np.linspace(startInterval, endInterval, abs(stepCount) / resolution)
	#
	# 	#convert each float to int (since interval ms must be int)
	# 	accProfile = [ int(element) for element in accProfile]
	#
	# 	accProfile.reverse()
	#
	# 	#send each runMotor command consecutively
	# 	r = len(accProfile)
	# 	for i in range(r):
	# 		wait = accProfile.pop()#time to wait in between steps
	#
	# 		#preserve direction
	# 		if(disp < 0):
	# 			self.runMotor_raw(motorName, -resolution, 1, True)
	# 		else:
	# 			self.runMotor_raw(motorName, resolution, 1, True)
	#
	# 		time.sleep(wait)


	def getMotorStatus(self, motorName):
		"""

		"""
		m1Active = ct.c_long() #1 for active 0 for stopped
		m2Active = ct.c_long() #1 for active 0 for stopped
		m1Steps = ct.c_long() #number of steps until complete
		m2Steps = ct.c_long() #number of steps until complete
		inputs = ct.c_long() #int from 0 -31 of bit pattern input

		self.stpLib.GetCurrentStatus(ct.byref( m1Active ), ct.byref( m2Active ), ct.byref( m1Steps ), ct.byref( m2Steps ), ct.byref( inputs ))

		if(motorName == 2):
			if(m1Active.value == 1):
				return True
			elif(m1Active.value == 0):
				return False
			else:
				return None
		else:
			if(m2Active.value == 1):
				return True
			elif(m2Active.value == 0):
				return False
			else:
				return None


	def waitInterupt(self, motorName):
		"""
		waitInterupt()

		pauses program while motor is occupied

		Parameters
		-------
		None

		Returns
		-------
		None
		"""
		checkOften = 0.001
		occupied = self.getMotorStatus(motorName)

		#print("\nbegin wait. MotorStatus = " + str(occupied) + "\n")
		while( occupied ):
			time.sleep(checkOften)
			occupied = self.getMotorStatus(motorName)
			#print("sleep")
		#print("\nend wait\n")

	# def dispToSteps(self, disp):
	# 	"""
	# 	dispToSteps(disp)
	#
	# 	converts linear displacement to number of steps needed for stepper motor
	#
	# 	Parameters
	# 	-------
	# 	disp : float specifying the distance for stage to move
	#
	# 	Returns
	# 	-------
	# 	steps : number of steps needed for stage to move disp
	# 	"""
	# 	return ( abs(int( math.floor(self.dispToRev(disp) * MCC.STEPS_PER_REV) )) )
	#
	# def dispToRev(self, disp):
	# 	"""
	# 	dispToRev(disp)
	#
	# 	converts linear displacement to number of revolutions needed for stepper motor
	#
	# 	Parameters
	# 	-------
	# 	disp : float specifying the distance for stage to move
	#
	# 	Returns
	# 	-------
	# 	revs : number of revolutions needed for stage to move disp
	# 	"""
	# 	if(self.inInches):
	# 		return (abs(disp) / MCC.IN_PER_REV)
	# 	else:
	# 		return (abs(disp) / MCC.CM_PER_REV)
	#
	# def speedToInterval(self, speed):
	# 	"""
	# 	speedToInterval(speed)
	#
	# 	converts linear speed to interval of motor impulse
	#
	# 	Parameters
	# 	-------
	# 	speed : float specifying the linear speed for stage to move at
	#
	# 	Returns
	# 	-------
	# 	interval : interval of motor impulse
	# 	"""
	# 	interval = 1
	#
	# 	if(self.inInches):
	# 		interval =  ( abs( int( (MCC.IN_PER_REV) / ((speed * MCC.STEPS_PER_REV) / (MCC.MS_PER_SEC)) ) ) )
	# 	else:
	# 		interval = ( abs( int( (MCC.CM_PER_REV) / ((speed * MCC.STEPS_PER_REV) / (MCC.MS_PER_SEC)) ) ) )
	#
	# 	#can't have interval of zero so round up to 1
	# 	if(interval == 0):
	# 		interval = 1
	#
	# 	return (interval)
