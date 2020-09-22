# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

import socket
import pygame as pg
from sys import exit
inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inter.connect(('192.168.1.59', 8080))

pg.init()
c = pg.time.Clock()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
try: joystick = pg.joystick.Joystick(0)
except pg.error: joystick = None
else: joystick.init()

axis_input = [0, 0]
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: exit()
        elif joystick and event.type == pg.JOYAXISMOTION:
            axis_input[event.axis] = event.value if abs(event.value) > 0.2 else 0
    c.tick(30)
    key_in = pg.key.get_pressed()
    light_sequence = ['0', '0', '0', '0']
    if joystick:
        if axis_input[0] < 0:
            light_sequence[1] = '1'
        elif axis_input[0] > 0:
            light_sequence[3] = '1'
        if axis_input[1] < 0:
            light_sequence[0] = '1'
        elif axis_input[1] > 0:
            light_sequence[2] = '1'
    else:
        for i in enumerate([pg.K_w, pg.K_a, pg.K_s, pg.K_d]):
            light_sequence[i[0]] = str(key_in[i[1]])
    light_string = ''.join(light_sequence).encode('utf-8')
    inter.sendall(light_string)
    pg.display.flip()

inter.close()
