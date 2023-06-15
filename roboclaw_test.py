from roboclaw import Roboclaw
from time import sleep

speed = 126
address = {
		1: 0x80, #front motors
		2: 0x81, #mid motors
		3: 0x82, #back motors
		4: 0x83, #front steering
		5: 0x84 #back steering
	}

roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

if __name__ == "__main__":
    
	roboclaw.BackwardM1(address[1], 0)
	roboclaw.BackwardM2(address[1], 0)
	roboclaw.BackwardM1(address[2], 0)
	roboclaw.BackwardM2(address[2], 0)
	roboclaw.BackwardM1(address[3], 0)
	roboclaw.BackwardM2(address[3], 0)
	sleep(2)
    
	print("init")
	roboclaw.ForwardM1(address[1], 64)
	print("forward 1")
	roboclaw.ForwardM2(address[1], 64)
	print("forward 2")
	roboclaw.ForwardM1(address[2], 64)
	print("middle 1")
	roboclaw.ForwardM2(address[2], 64)
	print("middle 2")
	roboclaw.ForwardM1(address[3], 64)
	print("back 1")
	roboclaw.ForwardM2(address[3], 64)
	print("back 2")
	sleep(5)
	
	roboclaw.BackwardM1(address[1], speed)
	roboclaw.BackwardM2(address[1], speed)
	roboclaw.BackwardM1(address[2], speed)
	roboclaw.BackwardM2(address[2], speed)
	roboclaw.ForwardM1(address[3], speed)
	roboclaw.ForwardM2(address[3], speed)

