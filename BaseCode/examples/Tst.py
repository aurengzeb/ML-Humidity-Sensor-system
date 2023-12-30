import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(13,gpio.OUT)
gpio.setup(19,gpio.OUT)
gpio.setup(5,gpio.IN)
gpio.setup(6,gpio.IN)
gpio.output(13,0)
gpio.output(19,0)

while True:
	if gpio.input(5) == 1:
		print("Run")
	else:
		print("Halt")
	if gpio.input(6) == 1:
		print("Do Data Collect")
	else:
		print("Use previous model")

	time.sleep(1)
