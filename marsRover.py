import RPi.GPIO as GPIO
import time
import socket

outs = [15, 7, 14, 18]


def setup():
	global inter
	GPIO.setmode(GPIO.BCM)

	for out in outs:
		GPIO.setup(out, GPIO.OUT)

def loop():
	global connection
	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind(('192.168.1.59', 8080))
	inter.listen(5)

	while True:
	    connection = inter.accept()[0]

		data = connection.recv(4096)
	    while not data:
	        data = connection.recv(4096)

		direction = data.split()
		print(data)
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
