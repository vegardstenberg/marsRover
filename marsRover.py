import RPi.GPIO as GPIO
import time
import socket

outs = [15, 7, 14, 18]

GPIO.setmode(GPIO.BCM)

for out in outs:
	GPIO.setup(out, GPIO.OUT)

inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inter.bind(('192.168.1.59', 8080))
inter.listen(5)

while True:
    connection = inter.accept()[0]

    while True:
        data = connection.recv(4096)
        if not data: break
	
	for key in enumerate(data):
		print(key)
		GPIO.output(outs[int(key[0])], int(key[1]))

    connection.close()

GPIO.cleanup()
