#import RPi.GPIO as GPIO
import time
import socket
from roboclaw import Roboclaw
import constants as c

#outs = [15, 7, 14, 18]

def setup():
	global inter
	global address1
	global address2
	global address3
	global roboclaw

	#GPIO.setmode(GPIO.BCM)

	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind((c.pi_ip, 8080))
	inter.listen(5)

	address1 = 0x80 //front motors
	address2 = 0x81 //mid motors
	address3 = 0x82 //back motors

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
			roboclaw.ForwardM1(address1, 64)
			roboclaw.ForwardM2(address1, 64
			roboclaw.ForwardM1(address3, 64)
			roboclaw.ForwardM2(address3, 64)
			print("forward")
		elif decoded_data[2] == '1':
			roboclaw.BackwardM1(address1, 64)
			roboclaw.BackwardM2(address1, 64)
			roboclaw.BackwardM1(address3, 64)
			roboclaw.BackwardM2(address3, 64)
			print("backwards")
		else:
			roboclaw.BackwardM1(address1, 0)
			roboclaw.BackwardM2(address1, 0)
			roboclaw.BackwardM1(address3, 0)
			roboclaw.BackwardM2(address3, 0)

		if decoded_data[1] == '1':
			roboclaw.ForwardM1(address2, 64)
			roboclaw.BackwardM2(address2, 64)
			print("left")
		elif decoded_data[3] == '1':
			roboclaw.ForwardM2(address2, 64)
			roboclaw.BackwardM1(address2, 64)
			print("right")
		else:
			roboclaw.BackwardM1(address2, 0)
			roboclaw.BackwardM2(address2, 0)

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
