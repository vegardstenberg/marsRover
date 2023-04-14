import serial

#! this code is written off of a datasheet for the OKDO LiDAR sensor, i have no idea if this is even close to correct
#! i just ended up having a sudden spark of imagination to start writing the self driving code

# Configure the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Start continuous measurement mode
ser.write(b'B')

# Read and print distance data
while True:
    # Read data from the sensor
    data = ser.readline().decode('ascii').strip()

    # Check if data is valid
    if data.startswith('DIST,'):
        # Parse distance value
        distance = int(data.split(',')[1])

        # Print distance value
        print(f"Distance: {distance} mm")
