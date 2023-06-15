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
    roboclaw.BackwardM1(address[4], speed)
    roboclaw.BackwardM2(address[4], speed)
    roboclaw.ForwardM1(address[5], speed)
    roboclaw.ForwardM2(address[5], speed)
    sleep(2)
    speed = 0
    roboclaw.BackwardM1(address[4], speed)
    roboclaw.BackwardM2(address[4], speed)
    roboclaw.ForwardM1(address[5], speed)
    roboclaw.ForwardM2(address[5], speed)
    sleep(2)
    speed = 126
    roboclaw.BackwardM1(address[5], speed)
    roboclaw.BackwardM2(address[5], speed)
    roboclaw.ForwardM1(address[4], speed)
    roboclaw.ForwardM2(address[4], speed)
    sleep(2)
    speed = 0
    roboclaw.BackwardM1(address[5], speed)
    roboclaw.BackwardM2(address[5], speed)
    roboclaw.ForwardM1(address[4], speed)
    roboclaw.ForwardM2(address[4], speed)