from roboclaw import Roboclaw
from time import sleep

if __name__ == "__main__":
    
    address = 0x80
    roboclaw = Roboclaw("/dev/ttyS0", 38400)
    print("Intit Complete")
    roboclaw.Open()
    
    while True:
        
        roboclaw.ForwardM1(address,64)
        sleep(2)
        roboclaw.ForwardM1(address,0)
        sleep(2)
        print("Running Idle")
        roboclaw.ForwardM2(address, 64)
        sleep(2)
        roboclaw.ForwardM2(address,0)
        sleep(2)
    
    

