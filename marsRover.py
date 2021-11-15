#import RPi.GPIO as GPIO
import time
import socket
from io import BlockingIOError
from roboclaw import Roboclaw
import constants as c
from datetime import datetime as dt, timedelta as td
from time import sleep
socket.setdefaulttimeout(10)

class Queue(dict):
	def next(self, return_object='item'):
		return get_attr(self, return_object + 's')()[-1]

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

def drive(speed):
	print((speed, type(speed)))
	roboclaw.ForwardM1(address1, speed)
	roboclaw.ForwardM2(address1, speed)
	roboclaw.ForwardM1(address2, speed)
	roboclaw.ForwardM2(address2, speed)
	roboclaw.ForwardM1(address3, speed)
	roboclaw.ForwardM2(address3, speed)
	print('drive')

def reverse(speed):
	roboclaw.BackwardM1(address1, speed)
	roboclaw.BackwardM2(address1, speed)
	roboclaw.BackwardM1(address2, speed)
	roboclaw.BackwardM2(address2, speed)
	roboclaw.BackwardM1(address3, speed)
	roboclaw.BackwardM2(address3, speed)
	print('reverse')

def turn_left(speed):
	roboclaw.ForwardM1(address1, speed)
	roboclaw.BackwardM2(address1, speed)
	roboclaw.ForwardM1(address2, speed)
	roboclaw.BackwardM2(address2, speed)
	roboclaw.ForwardM1(address3, speed)
	roboclaw.BackwardM2(address3, speed)
	print('turn left')

def turn_right(speed):
	roboclaw.ForwardM2(address1, speed)
	roboclaw.BackwardM1(address1, speed)
	roboclaw.ForwardM2(address2, speed)
	roboclaw.BackwardM1(address2, speed)
	roboclaw.ForwardM2(address3, speed)
	roboclaw.BackwardM1(address3, speed)
	print('turn right')

def stop():
	roboclaw.BackwardM1(address1, 0)
	roboclaw.BackwardM2(address1, 0)
	roboclaw.BackwardM1(address2, 0)
	roboclaw.BackwardM2(address2, 0)
	roboclaw.BackwardM1(address3, 0)
	roboclaw.BackwardM2(address3, 0)
	print('stop')

queue = Queue()
txt_speed = 128
txt_turn = 0
args = {
	'drive': ('txt_speed',)
}

def get_events(data):
	if data == 'stop': return data
	data = data.split('|')
	return ({args[0]: args[1:]} for args in (command.split() for command in data))

def loop(local_testing=False):
	global connection
	global now
	while True:
		try:
			connection = inter.accept()[0]
			connection.setblocking(0)
		except socket.timeout: print('Can\'t find a cient-side machine to connect to. Attempting to reconnect...')
		else: break
	while True:
		now = dt.now() #Updates the time on every iteration
		try: data = connection.recv(4096)
		except BlockingIOError:
			data = None
			continue
		text_controls = False
		if data:
			data = data.decode('utf-8').split('&')[-1]
			text_controls = data[0]
			data = data[1:]
			if text_controls:
				get_events(data)
		'''
		execute_commands = data.split('|')
		for time, cmd in future_commands.copy().items():
			if now <= time: continue
			execute_commands.append(cmd)
			del future_commands[time]
		for command in execute_commands:
			print(f'Executing command: {command}')
			command = command.split(' ')
			if command[0] != 'stop':
				future_commands[now + td(seconds=int(command[1]))] = 'stop'
				if not local_testing: globals()[command[0]](*(globals()[arg_name] for arg_name in args[command[0]]))
			elif not local_testing: stop()

		if text_controls:
			print('Text controls are on')
			continue
		'''
		if data:
			speed = int(data[4:12], 2) // 2
			steering = int(data[12:20], 2)
			print('Speed: ' + str(speed) + ' | Steering: ' + str(steering))

		if local_testing: continue
		if data[0] == '1': drive(speed)
		elif data[2] == '1': reverse(speed)
		elif data[1] == '1': turn_left(speed)
		elif data[3] == '1': turn_right(speed)
		else: stop()

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
			print('Setup completed with ip "' + new_ip + '"')
		elif retry_query == 2:
			setup(ip='localhost')
			local_testing = True
			print('Setup completed in local test environment. Running without motors')
		else: exit()
	print("Running")
	try: loop(local_testing)
	except KeyboardInterrupt: stop()
