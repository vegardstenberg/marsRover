from roboclaw import Roboclaw

address = 0x80
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

if __name__ == "__main__":
	while True:
		roboclaw.ForwardM1(address[1], 64)
		roboclaw.ForwardM2(address[1], -64)
		roboclaw.ForwardM1(address[2], 64)
		roboclaw.ForwardM2(address[2], -64)
		roboclaw.ForwardM1(address[3], 64)
		roboclaw.ForwardM2(address[3], -64)
