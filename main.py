import MotorControl as mc

ss = mc.MotorControl()

ss.runMotor_raw(2, 101, 200)
# ss.runMotor_byInterval('x', 1.5, 3)

# ss.runMotor_byInterval('y', 0.1, 3)
# ss.runMotor_byInterval('x', -1.25, 3)

# raw_input("\nMotor(s) Running...\nPress Return...")
print '\nMotor Running...'

ss.waitInterupt(2)


raw_input("\nTasks Complete\nPress Return... ")
