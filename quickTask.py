import MotorControl as mc

ss = mc.MotorControl()

ss.runMotor_byInterval('y', -0.7, 3)
# ss.runMotor_byInterval('x', 1.5, 3)

# ss.runMotor_byInterval('y', 0.1, 3)
# ss.runMotor_byInterval('x', -1.25, 3)

# raw_input("\nMotor(s) Running...\nPress Return...")
# print '\nMotor(s) Running...'

ss.waitInterupt('y')
ss.waitInterupt('x')

raw_input("\nTasks Complete\nPress Return... ")