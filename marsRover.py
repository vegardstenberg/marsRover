#import RPi.GPIO as GPIO
import time
import socket
from roboclaw import Roboclaw

outs = [15, 7, 14, 18]

def setup():
	global inter
	global address
	global roboclaw

	#GPIO.setmode(GPIO.BCM)

	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind(('192.168.1.59', 8080))
	inter.listen(5)

	address = 0x80
	roboclaw = Roboclaw("/dev/ttyS0", 38400)
	roboclaw.Open()

	#for out in outs:
	#	GPIO.setup(out, GPIO.OUT)

	print("Setting up")

def loop():
	global connection

	print("Running")

	while True:
	    connection = inter.accept()[0]

	    while True:
	        data = connection.recv(4096)
	        if not data: break

		data = data[-4:]
		decoded_data = data.decode('utf-8')

		if decoded_data[0] == '1':
			roboclaw.ForwardM1(address, 64)
			#roboclaw.ForwardM2(address, 64)
		else:
			roboclaw.ForwardM1(address, 0)
			#roboclaw.ForwardM2(address, 0)

		if decoded_data[2] == '1':
			roboclaw.BackwardM1(address, 64)
			#roboclaw.BackwardM2(address, 64)
			print("forward")
		else:
			roboclaw.BackwardM1(address, 0)
			#roboclaw.BackwardM2(address, 0)

		if decoded_data[1] == '1':
			print("left")

		if decoded_data[3] == '1':
			print("right")

		#for key in enumerate(data):
		#	GPIO.output(outs[int(key[0])], int(key[1]))

def stop():
	connection.close()
	#GPIO.cleanup()
	print("Stopping")

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt: #Exception as e:
		#print(e)
		stop()
