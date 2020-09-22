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

<<<<<<< HEAD
=======
	direction = data.split()

	if(direction[0] == 1)
	{
		print("forward")
	} elif(direction[1] == 1)
	{
		print("backwards")
	}

	if(direction[2] == 1)
	{
		print("right")
	} elif(direction[3] == 1)
	{
		print("left")
	}

>>>>>>> 16d136c9d3f871e6cdec90f490336aa0dabbc833
	for key in enumerate(data):
		print(key)
		GPIO.output(outs[int(key[0])], int(key[1]))

    connection.close()

GPIO.cleanup()
