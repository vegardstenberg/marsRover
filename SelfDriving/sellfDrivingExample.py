import time
from roboclaw import Roboclaw

# Initialize the Roboclaw controller
address = 0x80
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()
roboclaw.ResetEncoders(address)
random = int

# Set the speed of the rover
speed = 256

# Define a function to drive the rover forward
def drive_forward():
    roboclaw.ForwardM1(address, speed)
    roboclaw.ForwardM2(address, speed)

# Define a function to drive the rover backward
def drive_backward():
    roboclaw.BackwardM1(address, speed)
    roboclaw.BackwardM2(address, speed)

# Define a function to turn the rover left
def turn_left():
    roboclaw.ForwardM1(address, speed)
    roboclaw.BackwardM2(address, speed)

# Define a function to turn the rover right
def turn_right():
    roboclaw.BackwardM1(address, speed)
    roboclaw.ForwardM2(address, speed)

# Define a function to stop the rover
def stop():
    roboclaw.ForwardM1(address, 0)
    roboclaw.ForwardM2(address, 0)

# Define a function to read the distance from an obstacle
def read_distance():
    # Code to read distance from a sensor goes here
    # This will depend on the type of sensor you are using

# Define the main loop for 1 sensor
    """  
# This code would be for one sensor; i believe using 2 sensors like how a robot cleaner does, would benefit a lot.
while True:
    distance = read_distance()
    
    # If the distance is less than a certain threshold, stop and turn
    if distance < 10:
        stop()
        
        # Choose a random direction to turn
        if random.randint(0, 1) == 0:
            turn_left()
        else:
            turn_right()
            
        # Wait for a short period to complete the turn
        time.sleep(1)
    else:
         Drive forward
        drive_forward()
        
    # Wait for a short period before reading the distance again
    time.sleep(0.1) """

# Define the main loop for 2 sensors
while True: # Here is the improved code
    # Read the state of the sensors
    left_sensor, right_sensor = read_distance()
    
    # If both sensors detect an obstacle, stop and turn around
    if left_sensor and right_sensor:
        stop()
        drive_backward()
        time.sleep(1)
        turn_left()
        time.sleep(1)
    # If only the left sensor detects an obstacle, turn right
    elif left_sensor:
        stop()
        turn_right()
        time.sleep(1)
    # If only the right sensor detects an obstacle, turn left
    elif right_sensor:
        stop()
        turn_left()
        time.sleep(1)
    # Otherwise, drive forward
    else:
        drive_forward()
        
    # Wait for a short period before reading the sensor values again
    time.sleep(0.1)

# ! Future implementation would most likely be to give it a certain area based on coordinates to drive.
# ! I've based this entire code off of how a robot cleaner does its job
## I did some research into how self driving cars work, and a recomended type of sensor would be LIDAR sensors.
## Enviormental sensoring would also be suitable for a mars rover