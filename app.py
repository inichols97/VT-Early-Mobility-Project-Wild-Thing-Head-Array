# Wild Things Head Array
# Main script
# Version 1.4
# 11/17/2019

# Do not change any of the imports
import RPi.GPIO as PIN
import time as t
import constants as c

# I've disabled  false errors and set the configuration for the GPIO pin layout
# warnings
PIN.setwarnings(False)
# pin layout
PIN.setmode(PIN.BOARD)

def Main():

	# Default control set
	defaultControls = c.defaultControlSet
	# Edit the default control set here

	print("Initializing")
	# Set the GPIO pins for the sensor output
	trigLeft = 3
	trigBack = 5
	trigRight = 7
	# Set the GPIO pins for the sensor input
	echoRight = 11
	echoLeft = 13
	echoBack = 15
	# Set the GPIO pins for the functional output
	lightBack = 8
	lightRight = 10
	lightLeft = 12
	# These lights correspond to the motors that would be activated
	motorLeft = 16
	motorRight = 18

	# Initialize the Kill switch
	T0 = 29
	A = 31
	B = 33
	C = 35
	D = 37
	PIN.setup(T0, PIN.IN)
	PIN.setup(A, PIN.IN)
	PIN.setup(B, PIN.IN)
	PIN.setup(C, PIN.IN)
	PIN.setup(D, PIN.IN)
	killCommand = False
	channelStateA = False
	channelStateB = False
	channelStateC = False
	channelStateD = False

	# Initialize the restart switch
	restart = 36
	PIN.setup(restart, PIN.IN)
	restartCommand = False

	# Initialize all of the pins for input, output, and function
	PIN.setup(trigLeft, PIN.OUT)
	PIN.setup(trigBack, PIN.OUT)
	PIN.setup(trigRight, PIN.OUT)

	PIN.setup(echoLeft, PIN.IN)
	PIN.setup(echoBack, PIN.IN)
	PIN.setup(echoRight, PIN.IN)

	PIN.setup(lightLeft, PIN.OUT)
	PIN.setup(lightBack, PIN.OUT)
	PIN.setup(lightRight, PIN.OUT)
	# Let the raspberry pi pause for a moment to start the sensors
	t.sleep(0.1)
	print("Sensors Starting Up...")
	# Sensors started

	# get control selection
	controlSet = controlSelect()
	# 1 Control set for LEFT-sensor --> forward movement
	# 2 Control set for RIGHT-sensor --> forward movement
	# 3 Control set for BACK-sensor --> forward movement
	# 4 Control set for RIGHT-sensor --> forward movement & LEFT-sensor --> left turn
	# 5 Control set for LEFT-sensor --> forward movement & RIGHT-sensor --> right turn
	# 6 Control set for BACK-sensor --> forward movement & LEFT-sensor --> left turn & RIGHT-sensor --> right turn
	if(controlSet == 0)
		controlSet = defaultControls

	# This statement is only True when the kill switch has not been activated
	# Kill switch added in version 1.2
	prevLeft = c.prevSets
	prevBack = c.prevSets
	prevRight = c.prevSets
	forward = False
	leftTurn = False
	rightTurn = False
	sustain = 0
	while not killCommand:
		switch (controlSet) {
			case 1:
				timeLeft = leftSensors()
				# Calculate the distances from each sensor to the patient
				disLeft = (timeLeft * 17000)
				# Print the distances
				print("Left:")
				print(disLeft)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disLeft < 999999999 and disLeft < (prevLeft + 1000):
					print("moving Forward")
					PIN.output(lightLeft, PIN.HIGH)
					sustain = sustain + 1
				else
					sustain = 0
					forward = 0
					left = 0
					right = 0

				if sustain >= 5
					forward = True
					PIN.output(motorLeft, PIN.HIGH)
					PIN.output(motorRight, PIN.HIGH)
					t.sleep(0.001)
					PIN.output(motorLeft, PIN.LOW)
					PIN.output(motorRight, PIN.LOW)

				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)
				prevLeft = disLeft
			case 2:
				timeRight = rightSensors()
				# Calculate the distances from each sensor to the patient
				disRight = (timeRight * 17000)
				# Print the distances
				print("Right:")
				print(disRight)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disRight < 999999999 and disRight < (prevRight + 1000):
					print("moving Forward")
					PIN.output(lightRight, PIN.HIGH)
					sustain = sustain + 1
				else
					sustain = 0
					forward = 0
					left = 0
					right = 0

				if sustain >= 5
					forward = True
					PIN.output(motorLeft, PIN.HIGH)
					PIN.output(motorRight, PIN.HIGH)
					t.sleep(0.001)
					PIN.output(motorLeft, PIN.LOW)
					PIN.output(motorRight, PIN.LOW)

				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)
				prevRight = disRight
			case 3:
				timeBack = backSensors()
				# Calculate the distances from each sensor to the patient
				disBack = (timeBack * 17000)
				# Print the distances
				print("Back:")
				print(disBack)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disBack < 999999999 and disBack < (prevBack + 1000):
					print("moving Forward")
					PIN.output(lightBack, PIN.HIGH)
					sustain = sustain + 1
				else
					sustain = 0
					forward = 0
					left = 0
					right = 0

				if sustain >= 5
					forward = True
					PIN.output(motorLeft, PIN.HIGH)
					PIN.output(motorRight, PIN.HIGH)
					t.sleep(0.001)
					PIN.output(motorLeft, PIN.LOW)
					PIN.output(motorRight, PIN.LOW)

				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)
				prevBack = disBack
			case 4:
				timeLeft = leftSensors()
				timeRight = rightSensors()

				# Calculate the distances from each sensor to the patient
				disLeft = (timeLeft * 17000)
				disRight = (timeRight * 17000)
				# Print the distances
				print("Left:")
				print(disLeft)
				print("Right:")
				print(disRight)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disLeft < disBack and disLeft < disRight:
					print("moving Left")
					PIN.output(lightLeft, PIN.HIGH)
				elif disBack < disLeft and disBack < disRight:
					print("moving Back")
					PIN.output(lightBack, PIN.HIGH)
				elif disRight < disLeft and disRight < disBack:
					print("moving Right")
					PIN.output(lightRight, PIN.HIGH)
				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)
			case 5:
				timeLeft = leftSensors()
				timeBack = backSensors()
				timeRight = rightSensors()

				# Calculate the distances from each sensor to the patient
				disLeft = (timeLeft * 17000)
				disBack = (timeBack * 17000)
				disRight = (timeRight * 17000)
				# Print the distances
				print("Left:")
				print(disLeft)
				print("Back:")
				print(disBack)
				print("Right:")
				print(disRight)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disLeft < disBack and disLeft < disRight:
					print("moving Left")
					PIN.output(lightLeft, PIN.HIGH)
				elif disBack < disLeft and disBack < disRight:
					print("moving Back")
					PIN.output(lightBack, PIN.HIGH)
				elif disRight < disLeft and disRight < disBack:
					print("moving Right")
					PIN.output(lightRight, PIN.HIGH)
				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)
			case 6:
				timeLeft = leftSensors()
				timeBack = backSensors()
				timeRight = rightSensors()

				# Calculate the distances from each sensor to the patient
				disLeft = (timeLeft * 17000)
				disBack = (timeBack * 17000)
				disRight = (timeRight * 17000)
				# Print the distances
				print("Left:")
				print(disLeft)
				print("Back:")
				print(disBack)
				print("Right:")
				print(disRight)

				# Determine which sensor is being triggered
				# The sensor closest to the patient should trigger
				if disLeft < disBack and disLeft < disRight:
					print("moving Left")
					PIN.output(lightLeft, PIN.HIGH)
				elif disBack < disLeft and disBack < disRight:
					print("moving Back")
					PIN.output(lightBack, PIN.HIGH)
				elif disRight < disLeft and disRight < disBack:
					print("moving Right")
					PIN.output(lightRight, PIN.HIGH)
				if PIN.input(kill) == 1:
					killCommand = True
				t.sleep(0.5)
				# kill all functional output
				PIN.output(lightLeft, PIN.LOW)
				PIN.output(lightBack, PIN.LOW)
				PIN.output(lightRight, PIN.LOW)

	# kill all functional output
	PIN.output(lightLeft, PIN.LOW)
	PIN.output(lightBack, PIN.LOW)
	PIN.output(lightRight, PIN.LOW)
	print("Stopping...")
	# Deactivate pins and clear all active function
	# PIN.cleanup()

	while not restartCommand:
		if PIN.input(31) == 1:
			print("Restarting...")
			restartCommand = True
		if PIN.input(29) == 1:
			print("Exit")
			PIN.output(lightLeft, PIN.LOW)
			PIN.output(lightBack, PIN.LOW)
			PIN.output(lightRight, PIN.LOW)
			PIN.cleanup()
	t.sleep(0.5)
	Main()
	return

def leftSensors():
	# Left
	# Sensor output
	PIN.output(trigLeft, PIN.HIGH)
	t.sleep(c.sensorWait)
	PIN.output(trigLeft, PIN.LOW)

	# sensor input
	while PIN.input(echoLeft) == 0:
		pass
	startLeft = t.time()

	while PIN.input(echoLeft) == 1:
		pass
	stopLeft = t.time()
	timeLeft = stopLeft - startLeft

def backSensors():
	# Back
	PIN.output(trigBack, PIN.HIGH)
	t.sleep(c.sensorWait)
	PIN.output(trigBack, PIN.LOW)

	while PIN.input(echoBack) == 0:
		pass
	startBack = t.time()

	while PIN.input(echoBack) == 1:
		pass
	stopBack = t.time()
	timeBack = stopBack - startBack

def rightSensors():
	# Right
	PIN.output(trigRight, PIN.HIGH)
	t.sleep(c.sensorWait)
	PIN.output(trigRight, PIN.LOW)

	while PIN.input(echoRight) == 0:
		pass
	startRight = t.time()

	while PIN.input(echoRight) == 1:
		pass
	stopRight = t.time()
	timeRight = stopRight - startRight


# Press channel A button on fob to select control scheme
def controlSelect():
	channel = 0
	while(PIN.input(D) == 0):
		# listen for fob press
		if PIN.input(A):
			channel++
			# print out current count
			print(channel)
		# clear count if Channel B is pressed
		if PIN.input(B):
			channel = 0
	# Confirm selection if channel D is selected
	return channel

# Sustained pressure = movement

Main()
