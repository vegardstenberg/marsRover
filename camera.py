import cv2
import pygame
import numpy as np
import sys as sus

#0 Is the built in camera.
cap = cv2.VideoCapture(0)
#Gets fps of your camera
fps = cap.get(cv2.CAP_PROP_FPS)
#print("fps:", fps)
#If your camera can achieve 60 fps
#Else just have this be 1-30 fps
cap.set(cv2.CAP_PROP_FPS, 60)


def get_frame():

    success, frame = cap.read()
    if not success:
        return

    #for some reasons the frames appeared inverted
    # frame = np.fliplr(frame)
    frame = np.rot90(frame)

    # The video uses BGR colors and PyGame needs RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    surf = pygame.surfarray.make_surface(frame)

    # Show the PyGame surface!
    return surf