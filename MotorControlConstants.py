#define all motor control constants for stepperbee program
#Jake Meth - 2013 08 05

CM_PER_IN = 2.54 #2.54 cm per inch
MS_PER_SEC = 1000.0 #1000 milliseconds per second
IN_PER_REV = 0.020 #1 rev = 0.020 in of linear travel
CM_PER_REV = IN_PER_REV * CM_PER_IN #1 rev = 0.0508 cm of linear travel
STEPS_PER_REV = 200.0 #number of stepps the stepper motor must complete to rotate 360 deg
MAX_LIN_SPEED_CM = (CM_PER_REV) / ( (1.0 * STEPS_PER_REV) / (MS_PER_SEC) ) #max speed of stage is 0.254 cm/s
MAX_LIN_SPEED_IN = (IN_PER_REV) / ( (1.0 * STEPS_PER_REV) / (MS_PER_SEC) ) #max speed of stage is 0.1 in/s