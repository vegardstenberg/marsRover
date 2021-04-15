import socket
import cv2
import constants as c

s = socket.socket()
s.bind((c.pi_ip, 8080))

s.listen(5)
c, addr = s.accept()
vid = cv2.VideoCapture(0)

print('Got connection from', addr)

while True:
    ret, frame = vid.read()

    c.send(frame.encode())

    print("From Client: ", c.recv(1024))

c.close()
vid.release()
