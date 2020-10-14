import RPi.GPIO as GPIO
import time
import socket

outs = [15, 7, 14, 18]

def setup():
	global inter
	GPIO.setmode(GPIO.BCM)

	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind(('192.168.1.59', 8080))
	inter.listen(5)

	for out in outs:
		GPIO.setup(out, GPIO.OUT)

	print("Setting up")

def loop():
	global connection

	print("Running")

	while True:
	    connection = inter.accept()[0]

	    while True:
	        data = connection.recv(4096)
	        if data: break

		decoded_data = data[-4:].decode('utf-8')

		if decoded_data[0] == '1':
			print("forward")

		elif decoded_data[2] == '1':
			print("backwards")

		if decoded_data[1] == '1':
			print("left")

		elif decoded_data[3] == '1':
			print("right")

		for key in enumerate(data):
			GPIO.output(outs[int(key[0])], int(key[1]))

def stop():
	connection.close()
	GPIO.cleanup()
	print("Stopping")

if __name__ == '__main__':
	setup()
	try:
		loop()
	except:
		stop()
