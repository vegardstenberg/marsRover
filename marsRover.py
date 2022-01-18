#import RPi.GPIO as GPIO
import time
import socket
from io import BlockingIOError
from roboclaw import Roboclaw
import constants as c
from datetime import datetime as dt, timedelta as td
from time import sleep
socket.setdefaulttimeout(10)

class Event:
	def __init__(self, duration=0):
		self.duration = td(seconds=duration)
	def run(self):
		return

class Events:
	class ActionEvent(Event):
		def __init__(self, duration=0):
			self.duration = td(seconds=duration)
	class DriveEvent(ActionEvent):
		def run(self, **kwargs):
			drive(kwargs["speed"])

	class ReverseEvent(ActionEvent):
		def run(self, **kwargs):
			reverse(kwargs["speed"])

	class TurnLeftEvent(ActionEvent):
		def run(self, **kwargs):
			turn_left(kwargs["turning"])

	class TurnRightEvent(ActionEvent):
		def run(self, **kwargs):
			turn_right(kwargs["turning"])

	class StopEvent(ActionEvent):
		def run(self, **kwargs):
			stop()


	class SetupEvent(Event): pass
	class SetSpeedEvent(Event):
		def __init__(self, speed):
			self.speed = speed

		def run(self):
			return ("speed", self.speed)

class Queue(list):
	def __init__(self):
		self.endtime = None
		self.speed = 127
		self.turning = 0

	def append(self, event):
		event.runtime = self.endtime if self.endtime else now
		self.endtime = event.endtime = event.runtime + event.duration
		super().append(event)

	def run_next(self):
		event = self.pop(0)
		if isinstance(event, Events.ActionEvent):
			event.run(**self.run_kwargs)
		elif isinstance(event, Events.SetupEvent):
			setattr(self, *event.run())

	@property
	def run_kwargs(self):
		return {"speed": self.speed, "turning": self.turning}
queue = Queue()

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
	print("drive")
	if not local_testing:
		roboclaw.ForwardM1(address1, speed)
		roboclaw.ForwardM2(address1, speed)
		roboclaw.ForwardM1(address2, speed)
		roboclaw.ForwardM2(address2, speed)
		roboclaw.ForwardM1(address3, speed)
		roboclaw.ForwardM2(address3, speed)

def reverse(speed):
	print("reverse")
	if not local_testing:
		roboclaw.BackwardM1(address1, speed)
		roboclaw.BackwardM2(address1, speed)
		roboclaw.BackwardM1(address2, speed)
		roboclaw.BackwardM2(address2, speed)
		roboclaw.BackwardM1(address3, speed)
		roboclaw.BackwardM2(address3, speed)

def turn_left(speed):
	print("turn left")
	if not local_testing:
		roboclaw.ForwardM1(address1, speed)
		roboclaw.BackwardM2(address1, speed)
		roboclaw.ForwardM1(address2, speed)
		roboclaw.BackwardM2(address2, speed)
		roboclaw.ForwardM1(address3, speed)
		roboclaw.BackwardM2(address3, speed)

def turn_right(speed):
	print("turn right")
	if not local_testing:
		roboclaw.ForwardM2(address1, speed)
		roboclaw.BackwardM1(address1, speed)
		roboclaw.ForwardM2(address2, speed)
		roboclaw.BackwardM1(address2, speed)
		roboclaw.ForwardM2(address3, speed)
		roboclaw.BackwardM1(address3, speed)

def stop():
	print("stop")
	if not local_testing:
		value = 0
		roboclaw.BackwardM1(address1, value)
		roboclaw.BackwardM2(address1, value)
		roboclaw.BackwardM1(address2, value)
		roboclaw.BackwardM2(address2, value)
		roboclaw.BackwardM1(address3, value)
		roboclaw.BackwardM2(address3, value)

queue = Queue()
txt_speed = 128
txt_turn = 0
args = {
	"drive": ("txt_speed",)
}

def get_events(data):
	if data == "stop": return data
	data = data.split("|")
	return ({args[0]: args[1:]} for args in (command.split() for command in data))

def loop():
	global connection
	global now
	while True:
		try:
			connection = inter.accept()[0]
			connection.setblocking(0)
		except socket.timeout: print("Can't find a cient-side machine to connect to. Attempting to reconnect...")
		else: break
	text_controls = False
	while True:
		try:
			now = dt.now() #Updates the time on every iteration
			try: data = connection.recv(4096)
			except BlockingIOError: data = None
			if data:
				data = data.decode("utf-8").replace("&&", "&").split("&")[-2]
				text_controls = data[0]
				data = data[1:]
				if text_controls:
					for command in (arg.strip(" ") for arg in data.split("|")):
						command = [arg.strip(" ") for arg in command.split(",")]
						event_type = getattr(Events, f"{command[0].title().replace(" ", "")}Event")
						event = event_type(int(command[1]))
						queue.append(event)

				else:
					speed = int(data[4:12], 2) // 2
					steering = int(data[12:20], 2)
					print("Speed: " + str(speed) + " | Steering: " + str(steering))
					if local_testing: continue
					if data[0] == "1": drive(speed)
					elif data[2] == "1": reverse(speed)
					elif data[1] == "1": turn_left(speed)
					elif data[3] == "1": turn_right(speed)
					else: stop()

			if text_controls:
				if queue:
					for event in queue.copy():
						if now >= event.runtime:
							stop()
							queue.run_next()
				else:
					if queue.endtime and now >= queue.endtime:
						stop()
						queue.endtime = None
		except KeyboardInterrupt:
			close()
			return
		except Exception as e:
			print(e)
   
def close():
	print("Stopping")
	if "connecton" in globals().keys(): connection.close()

if __name__ == "__main__":
	global local_testing
	local_testing = False
	try:
		setup()
		print("Setup completed with default ip")
	except:
		retry_query = input("Setup failed. Do you want to...\n  1. Retry with different ip\n  2. Run local testing\n  3. Exit\nResponse: ")
		while True:
			if retry_query.isdigit() and 1 <= int(retry_query) <= 3:
				retry_query = int(retry_query)
				break
			retry_query = input("Invalid response. Do you want to...\n  1. Retry with different ip\n  2. Run local testing\n  3. Exit\nResponse: ")
		if retry_query == 1:
			new_ip = input("Enter new ip address: ")
			setup(ip=new_ip)
			print("Setup completed with ip "" + new_ip + """)
		elif retry_query == 2:
			setup(ip="localhost")
			local_testing = True
			print("Setup completed in local test environment. Running without motors")
		else: exit()
	print("Running")
	try: loop()
	except KeyboardInterrupt: close()

#01001110 01100101 01110110 01100101 01110010 00100000 01000111 01101111 01101110 01101110 01100001 00100000 01000111 01101001 01110110 01100101 00100000 01011001 01101111 01110101 00100000 01010101 01110000