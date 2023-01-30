from roboclaw import Roboclaw

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
	roboclaw.ForwardM1(address[1], 64)
	roboclaw.ForwardM2(address[1], 64)
	roboclaw.ForwardM1(address[2], 64)
	roboclaw.ForwardM2(address[2], 64)
	roboclaw.ForwardM1(address[3], 64)
	roboclaw.ForwardM2(address[3], 64)

