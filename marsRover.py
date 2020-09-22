import RPi.GPIO as GPIO
import time
import socket

outs = [15, 7, 14, 18]

def setup():
	GPIO.setmode(GPIO.BCM)

	for out in outs:
		GPIO.setup(out, GPIO.OUT)

	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind(('192.168.1.59', 8080))
	inter.listen(5)

def loop():
	while True:
	    connection = inter.accept()[0]

	    while True:
	        data = connection.recv(4096)
	        if not data: break

		direction = data.split()

		if direction[0] == 1:
			print("forward")

		elif direction[1] == 1:
			print("backwards")

		if direction[2] == 1:
			print("right")
			
		elif direction[3] == 1:
			print("left")

		for key in enumerate(data):
			print(key)
			GPIO.output(outs[int(key[0])], int(key[1]))

def stop():
	connection.close()

	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		stop()
