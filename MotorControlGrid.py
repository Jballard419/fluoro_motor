#Class used to control motors on scanning stage with stepperbee
#Jake Meeth - 2013 08 05

#gridCurve is not working

import ctypes as ct
import numpy as np
import math
import time
from collections import defaultdict, OrderedDict
import MotorControlConstants as MCC #user defined

class MotorControlGrid:
	"""
	
	"""
	def __init__(self, motorNames = ['x', 'y'], stepMode = 1, inInches = False, interupt = False):
		"""
		__init__(motorNames = ['x', 'y'], stepMode = 1, inInches = False, interupt = False)
	
		inititializes stepperbee
		
		Parameters
		-------
		motorNames : list of string names assigned to motor 1 and 2 respectively
		stepMode : 0 for wavestep, 1 for full step, 2 for power off
		inches : True to set default values to inches, False for cm
		interupt : True to set runMotor functions to wait for past call to finish
						
		Returns
		-------
		None
		"""
		#check that there is only 2 names
		if(len(motorNames) != 2):
			print("ERROR in '__init__(self, stepMode, inInches = False)'\n" + 
						"motorNames must be a length of 2\n")
		
		#hold names
		self.motorNames = motorNames
		
		#hold bool telling if values are in inches or cm
		self.inInches = inInches
		
		#hold bool telling interupt or not
		self.interupt = interupt
		
		#check that stepMode is proper value
		if( (stepMode < 0) or (stepMode > 2) ):
			print("ERROR in '__init__(self, stepMode, inInches = False)'\n" + 
						"stepMode must be an integer from 0 to 2\n")
		
		#initialize origin to be current location
		self.currentPos = [0, 0]
		
		#get reference to stepperbee library
		self.stpLib = ct.WinDLL('stp.dll')
		
		#initialize and set the stepping mode
		self.status = self.stpLib.InitStp()
		self.stpLib.SetStepMode(stepMode, stepMode)
		
		#Inform user of status
		print("Stepperbee connection status: " + str(self.status) + " devices connected")
	
	def runMotorGridCurve(self, xCurve, yCurve, speed):
		"""
		runMotorGridCurve(xCurve, yCurve, speed)
	
		moves stage to x, y position at desired speed
		
		Parameters
		-------
		xCurve : list specifying x points (must be same length as yCurve)
		yCurve : list specifying y points (must be same length as xCurve)
		speed : float specifying the speed for stage to move at (max speed = 0.254 cm/s or 0.1 in/s)
						
		Returns
		-------
		None
		"""
		#check that length of x and y are equal
		if(len(xCurve) != len(yCurve)):
			print("ERROR in 'runMotorGridCurve(self, xCurve, yCurve, speed)'\n" + 
						"xCurve and yCurve must have the same length\n")
			return
		
		for i in range(len(xCurve)):
			self.runMotorGridPoint(xCurve[i], yCurve[i], speed)
			self.waitInterupt(self.motorNames)
		
	def runMotorGridPoint(self, x, y, speed):
		"""
		runMotorGridPoint(x, y, speed)
	
		moves stage to x, y position at desired speed
		
		Parameters
		-------
		x : float specifying the x position
		y : float specifying the y position
		speed : float specifying the speed for stage to move at (max speed = 0.254 cm/s or 0.1 in/s)
						
		Returns
		-------
		None
		"""	
		#calculate distance to move in each direction
		deltaX = float(x) - self.currentPos[0]
		deltaY = float(y) - self.currentPos[1]
		
		#calculate speed for each direction to move in straight line
		# if(deltaX == 0):
			# speedX = 1 #doesnt actually contribute, cause no motion in this direction
			# speedY = speed
		# elif(deltaY == 0):
			# speedX = speed
			# speedY = 1
		# else:
			# speedX = abs( speed * np.cos(float(deltaY)/float(deltaX)) )
			# speedY = abs( speed * np.sin(float(deltaY)/float(deltaX)) )
			
		speedX = speed
		speedY = speed
		
		self.runMotor(self.motorNames[0], deltaX, speedX)
		self.runMotor(self.motorNames[1], deltaY, speedY)
		
		self.currentPos[0] = x
		self.currentPos[1] = y
		
		
	def runMotor(self, motorName, disp, speed):
		"""
		runMotor(motorName, disp, speed)
	
		moves motor disp(cm or in) at speed(cm/s or in/s)
		
		Parameters
		-------
		motorName : string corresponding to name of motor 1 or 2 givin to init
		disp : float specifying the distance for stage to move
		speed : float specifying the speed for stage to move at (max speed = 0.254 cm/s or 0.1 in/s)
						
		Returns
		-------
		steps : number of steps needed to move linear disp
		interval : motor interval impulse needed to move at speed
		"""
		steps = self.dispToSteps(disp)
		
		#make sure direction is preserved
		if(disp < 0):
			steps = steps * -1
		
		#check that speed isn't zero
		if(speed == 0):
			print("ERROR in 'runMotor(self, motorName, disp, speed)'\n" + 
						"speed can not be zero\n")
			return(None, None)
		
		#set interval		
		interval = self.speedToInterval(speed)
		
		#make sure direction is preserved
		if(speed < 0):
			steps = steps * -1
		
		#run motor
		self.runMotor_raw(motorName, steps, interval, self.interupt)
		
		return steps, interval

		
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
		motorNum = 0 #motor num is either 0 or 1
		if(motorName == self.motorNames[0]):
			motorNum = 1
		elif(motorName == self.motorNames[1]):
			motorNum = 0
		else:
			print("ERROR in 'runMotor_raw(self, motorName, steps, interval)'\n" + 
						"motorName not found\n")
			return
		
		#find direction for motor to run based on sign of steps
		#it is different for each motor
		direction = 0 #direction is either 0 or 1
		if( steps < 0 ):
			#direction must be negative
			if(motorNum == 1):
				direction = 1
			else: #motorNum must be 0
				direction = 0
		else:
			#direction must be positive
			if(motorNum == 1):
				direction = 0
			else: #motorNum must be 0
				direction = 1
		
		steps = abs(steps)
		
		#set outputs
		outputs = 0
		
		#run motor
		if(motorName == self.motorNames[1]):
			#check for motor interupt
			if(interupt):
				self.stpLib.RunMotor1(steps, interval, direction, outputs)
			else:
				self.waitInterupt(self.motorNames[0])
				self.stpLib.RunMotor1(steps, interval, direction, outputs)
			
		elif(motorName == self.motorNames[0]): #motorNum must be 0
			#check for motor interupt
			if(interupt):
				self.stpLib.RunMotor2(steps, interval, direction, outputs)
			else:
				self.waitInterupt(self.motorNames[1])
				self.stpLib.RunMotor2(steps, interval, direction, outputs)
				
		else:
			print("ERROR in 'runMotor_raw(self, motorName, steps, interval)'\n" + 
						"motorName not found\n")
			return None, None
		
		
	def runMotor_byInterval(self, motorName, disp, interval):
		"""
		runMotor(motorName, disp, interval)
	
		moves motor disp(cm or in) at interval(ms)
		
		Parameters
		-------
		motorName : string corresponding to name of motor 1 or 2 givin to init
		disp : float specifying the distance for stage to move
		interval : int specifying the speed for stage to move at (max speed = 0.254 cm/s at 1 ms interval)
						
		Returns
		-------
		steps : number of steps needed to move linear disp
		"""
		steps = self.dispToSteps(disp)
		
		#make sure direction is preserved
		if(disp < 0):
			steps = steps * -1
		
		#check that interval isnt negative
		if(interval < 0):
			print("ERROR in 'runMotor_byInterval(self, motorName, disp, interval)'\n" + 
						"interval cannot be negative\n")
			return(None)
		
		#run motor
		self.runMotor_raw(motorName, steps, interval, self.interupt)
		
		return steps
	
	def runMotorAcc_byInterval(self, motorName, disp, startInt, endInt, showInt = False):
		"""
		
		Pros: mostly accuate speeds
		Cons: pause between each speed change. Resolution of speeds is poor
		"""
			
		#find number of steps required
		stepCount = self.dispToSteps(abs(disp))
		
		#generate array of all intervals it must go through to be as uniform as possible
		#generate an equally spaced list of floats from start to finish
		accProfile = np.linspace(startInt, endInt, abs(stepCount))
		
		#convert each float to int (since interval ms must be int)
		accProfile = [ int(element) for element in accProfile]
		
		#count each occurence of each int in the profile
		#this way we can tell the motor to run 3 steps at an interval instead of 1 step at an interval
		#	and then again and again a third time
		summary = defaultdict(int)
		for i in accProfile:
			summary[i] += 1
		
		summaryItems = summary.items()
		if(startInt < endInt):
			summaryItems.reverse()
			
		summary = OrderedDict(summaryItems)

		#send each runMotor command consecutively
		r = len(summary)
		for i in range(r):
			task = summary.popitem() #task = (interval, steps)
			
			if(showInt):
				print task[0]
			
			#preserve direction
			if(disp < 0):
				self.runMotor_raw(motorName, -1 * task[1], task[0], False)
			else:
				self.runMotor_raw(motorName, task[1], task[0], False)

	def getMotorStatus(self, motorName):
		"""
		
		"""
		m1Active = ct.c_long() #1 for active 0 for stopped
		m2Active = ct.c_long() #1 for active 0 for stopped
		m1Steps = ct.c_long() #number of steps until complete
		m2Steps = ct.c_long() #number of steps until complete
		inputs = ct.c_long() #int from 0 -31 of bit pattern input
		
		self.stpLib.GetCurrentStatus(ct.byref( m1Active ), ct.byref( m2Active ), ct.byref( m1Steps ), ct.byref( m2Steps ), ct.byref( inputs ))
		
		if(motorName == self.motorNames[0]):
			if(m1Active.value == 1):
				return True
			elif(m1Active.value == 0):
				return False
			else:
				return None
		elif(motorName == self.motorNames[1]):
			if(m2Active.value == 1):
				return True
			elif(m2Active.value == 0):
				return False
			else:
				return None
		else:
			print("ERROR in 'getMotorStatus(self, motorName)'\n" + 
						"motorName not found\n")
			return None
		
	def waitInterupt(self, motorNames):
		"""
		waitInterupt()
	
		pauses program while motor is occupied
		
		Parameters
		-------
		motorNames = list of names to wait for. ['x', 'y']
						
		Returns
		-------
		None
		"""
		checkOften = 0.001
		occupied = False
		for i in range(len(motorNames)):
			if(self.getMotorStatus(motorNames[i])):
				occupied = True
			
		#print("\nbegin wait. MotorStatus = " + str(occupied) + "\n")
		while( occupied ):
			time.sleep(checkOften)
			occupied = False
			for i in range(len(motorNames)):
				if(self.getMotorStatus(motorNames[i])):
					occupied = True
			#print("sleep")
		#print("\nend wait\n")
		
	def dispToSteps(self, disp):
		"""
		dispToSteps(disp)
	
		converts linear displacement to number of steps needed for stepper motor
		
		Parameters
		-------
		disp : float specifying the distance for stage to move
						
		Returns
		-------
		steps : number of steps needed for stage to move disp
		"""
		return ( abs(int( math.floor(self.dispToRev(disp) * MCC.STEPS_PER_REV) )) )
		
	def dispToRev(self, disp):
		"""
		dispToRev(disp)
	
		converts linear displacement to number of revolutions needed for stepper motor
		
		Parameters
		-------
		disp : float specifying the distance for stage to move
						
		Returns
		-------
		revs : number of revolutions needed for stage to move disp
		"""
		if(self.inInches):
			return (abs(disp) / MCC.IN_PER_REV)
		else:
			return (abs(disp) / MCC.CM_PER_REV)
			
	def speedToInterval(self, speed):
		"""
		speedToInterval(speed)
	
		converts linear speed to interval of motor impulse
		
		Parameters
		-------
		speed : float specifying the linear speed for stage to move at
						
		Returns
		-------
		interval : interval of motor impulse
		"""
		interval = 1
		
		if(self.inInches):
			interval =  ( abs( int( (MCC.IN_PER_REV) / ((speed * MCC.STEPS_PER_REV) / (MCC.MS_PER_SEC)) ) ) )
		else:
			interval = ( abs( int( (MCC.CM_PER_REV) / ((speed * MCC.STEPS_PER_REV) / (MCC.MS_PER_SEC)) ) ) )
			
		#can't have interval of zero so round up to 1
		if(interval == 0):
			interval = 1
			
		return (interval)