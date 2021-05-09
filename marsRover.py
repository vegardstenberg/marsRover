#import RPi.GPIO as GPIO
import time
import socket
from roboclaw import Roboclaw
import constants as c
socket.setdefaulttimeout(10)

def setup(ip=c.pi_ip):
	global inter
	global address1
	global address2
	global address3
	global roboclaw

	inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	inter.bind((ip, 8080))
	inter.listen(5)

	address1 = 0x80 #front motors
	address2 = 0x81 #mid motors
	address3 = 0x82 #back motors

	roboclaw = Roboclaw("/dev/ttyS0", 38400)
	roboclaw.Open()

def loop(local_testing=False):
	global connection
	while True:
		try: connection = inter.accept()[0]
		except socket.timeout: print('Can\'t find a cient-side machine to connect to. Attempting to reconnect...')
		else: break
	while True:
		data = connection.recv(4096)
		if not data: break

		data = data[-20:]
		decoded_data = data.decode('utf-8')
		speed = int(data[4:12], 2) // 2
		steering = int(data[12:20], 2)
		print(f'Speed: {speed} | Steering: {steering} | Raw decoded data: {decoded_data}')

		if local_testing: continue
		if decoded_data[0] == '1':
			roboclaw.ForwardM1(address1, speed)
			roboclaw.ForwardM2(address1, speed)
			roboclaw.ForwardM1(address2, speed)
			roboclaw.ForwardM2(address2, speed)
			roboclaw.ForwardM1(address3, speed)
			roboclaw.ForwardM2(address3, speed)
			print("forward")
		elif decoded_data[2] == '1':
			roboclaw.BackwardM1(address1, speed)
			roboclaw.BackwardM2(address1, speed)
			roboclaw.BackwardM1(address2, speed)
			roboclaw.BackwardM2(address2, speed)
			roboclaw.BackwardM1(address3, speed)
			roboclaw.BackwardM2(address3, speed)
			print("backwards")
		elif decoded_data[1] == '1':
			roboclaw.ForwardM1(address1, speed)
			roboclaw.BackwardM2(address1, speed)
			roboclaw.ForwardM1(address2, speed)
			roboclaw.BackwardM2(address2, speed)
			roboclaw.ForwardM1(address3, speed)
			roboclaw.BackwardM2(address3, speed)
			print("left")
		elif decoded_data[3] == '1':
			roboclaw.ForwardM2(address1, speed)
			roboclaw.BackwardM1(address1, speed)
			roboclaw.ForwardM2(address2, speed)
			roboclaw.BackwardM1(address2, speed)
			roboclaw.ForwardM2(address3, speed)
			roboclaw.BackwardM1(address3, speed)
			print("right")
		else:
			roboclaw.BackwardM1(address1, 0)
			roboclaw.BackwardM2(address1, 0)
			roboclaw.BackwardM1(address2, 0)
			roboclaw.BackwardM2(address2, 0)
			roboclaw.BackwardM1(address3, 0)
			roboclaw.BackwardM2(address3, 0)

def stop():
	print("Stopping")
	if 'connecton' in globals().keys(): connection.close()

if __name__ == '__main__':
	local_testing = False
	try:
		setup()
		print('Setup completed with default ip')
	except:
		retry_query = input('Setup failed. Do you want to...\n  1. Retry with different ip\n  2. Run local testing\n  3. Exit\nResponse: ')
		while True:
			if retry_query.isdigit() and 1 <= int(retry_query) <= 3:
				retry_query = int(retry_query)
				break
			retry_query = input('Invalid response. Do you want to...\n  1. Retry with different ip\n  2. Run local testing\n  3. Exit\nResponse: ')
		if retry_query == 1:
			new_ip = input('Enter new ip address: ')
			setup(ip=new_ip)
			print(f'Setup completed with ip "{new_ip}"')
		elif retry_query == 2:
			setup(ip='localhost')
			local_testing = True
			print('Setup completed in local test environment. Running without motors')
		else: exit()
	print("Running")
	try: loop(local_testing)
	except KeyboardInterrupt: stop()
