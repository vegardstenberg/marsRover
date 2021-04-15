import socket
import cv2
import constants as c

s = socket.socket()
s.connect((c.pi_ip, 8080))
while True:
    try:
        cv2.imshow('frame', s.recv(1024).decode())
        s.send("Image recived!".encode())
    except:
        break
cv2.destroyAllWindows()
