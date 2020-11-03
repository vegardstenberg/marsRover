# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

import socket
import pygame as pg
from pygame import freetype
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
    c.tick(30)

    for event in pg.event.get():
        if event.type == pg.QUIT: exit()
        elif joystick and event.type == pg.JOYAXISMOTION:
            axis_input[event.axis] = event.value if abs(event.value) > 0.2 else 0

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

    w = pg.draw.rect(screen, (255, 255, 255), (110, 40, 100, 100))
    a = pg.draw.rect(screen, (255, 255, 255), (0, 150, 100, 100))
    s = pg.draw.rect(screen, (255, 255, 255), (110, 150, 100, 100))
    d = pg.draw.rect(screen, (255, 255, 255), (220, 150, 100, 100))

    if pg.mouse.get_pressed(1)[0]:
        if w.collidepoint(pg.mouse.get_pos()):
            light_sequence[1] = '1'
        if a.collidepoint(pg.mouse.get_pos()):
            light_sequence[0] = '1'
        if s.collidepoint(pg.mouse.get_pos()):
            light_sequence[2] = '1'
        if d.collidepoint(pg.mouse.get_pos()):
            light_sequence[3] = '1'

    light_string = ''.join(light_sequence).encode('utf-8')
    inter.sendall(light_string)
    cool_font = pg.freetype.SysFont('Arial', 70)

    text = {
        'w': cool_font.render('W'),
        'a': cool_font.render('A'),
        's': cool_font.render('S'),
        'd': cool_font.render('D'),
    }

    text['w'][1].center = w.center
    text['a'][1].center = a.center
    text['s'][1].center = s.center
    text['d'][1].center = d.center


    if int(light_sequence[0]):
        pg.draw.rect(screen, (255, 0, 0), (120, 50, 80, 80))
    if int(light_sequence[1]):
        pg.draw.rect(screen, (255, 0, 0), (10, 160, 80, 80))
    if int(light_sequence[2]):
        pg.draw.rect(screen, (255, 0, 0), (120, 160, 80, 80))
    if int(light_sequence[3]):
        pg.draw.rect(screen, (255, 0, 0), (230, 160, 80, 80))
    for i in ['w', 'a', 's', 'd']:
        screen.blit(*text[i])

    pg.display.flip()
    screen.fill((0, 0, 0))

inter.close()
