# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

import socket
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame import freetype
from sys import exit
from traceback import print_tb
import constants as c

def text_controls():
    print("Text controlls activated")

def fancy_controls():
    print("Fancy controlls activated.")

    pg.init()
    clk = pg.time.Clock()
    screen = pg.display.set_mode(c.pg_screen_res, pg.RESIZABLE)
    try: joystick = pg.joystick.Joystick(0)
    except pg.error: joystick = None
    else: joystick.init()

    axis_input = [0, 0]

    while True:
        clk.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT: exit() #Kasnskje disconnect fra roveren i stedet for bære sys.exit() her?
            elif joystick and event.type == pg.JOYAXISMOTION and event.axis < 2:
                axis_input[event.axis] = event.value if abs(event.value) > 0.2 else 0

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

        key_in = pg.key.get_pressed()
        for i in enumerate([pg.K_w, pg.K_a, pg.K_s, pg.K_d]):
            if light_sequence[i[0]] != 1: light_sequence[i[0]] = str(key_in[i[1]])

        w = pg.draw.rect(screen, c.rgb_white, (110, 40, 100, 100))
        a = pg.draw.rect(screen, c.rgb_white, (0, 150, 100, 100))
        s = pg.draw.rect(screen, c.rgb_white, (110, 150, 100, 100))
        d = pg.draw.rect(screen, c.rgb_white, (220, 150, 100, 100))

        if pg.mouse.get_pressed(1)[0]:
            if w.collidepoint(pg.mouse.get_pos()):
                light_sequence[0] = '1'
            if a.collidepoint(pg.mouse.get_pos()):
                light_sequence[1] = '1'
            if s.collidepoint(pg.mouse.get_pos()):
                light_sequence[2] = '1'
            if d.collidepoint(pg.mouse.get_pos()):
                light_sequence[3] = '1'

        if connect_query == 'y':
            light_string = ''.join(light_sequence).encode('utf-8')
            inter.sendall(light_string)

        text = {
            'w': c.font_arial.render('W'),
            'a': c.font_arial.render('A'),
            's': c.font_arial.render('S'),
            'd': c.font_arial.render('D'),
        }

        text['w'][1].center = w.center
        text['a'][1].center = a.center
        text['s'][1].center = s.center
        text['d'][1].center = d.center

        if int(light_sequence[0]):
            pg.draw.rect(screen, c.rgb_red, (120, 50, 80, 80))
        if int(light_sequence[1]):
            pg.draw.rect(screen, c.rgb_red, (10, 160, 80, 80))
        if int(light_sequence[2]):
            pg.draw.rect(screen, c.rgb_red, (120, 160, 80, 80))
        if int(light_sequence[3]):
            pg.draw.rect(screen, c.rgb_red, (230, 160, 80, 80))
        for i in ['w', 'a', 's', 'd']:
            screen.blit(*text[i])

        pg.display.flip()
        screen.fill((0, 0, 0))

if __name__ == '__main__':
    while True:
        connect_query = input('Want to connect to the rover? (y/n): ').lower()
        if connect_query == 'y':
            print("Trying to establish a connection with the rover...")
            try:
                inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                inter.connect((c.pi_ip, 8080))
            except:
                print('Could not connect to the rover. Continuing without connection...')
                connect_query = 'n'
            else: print("Connection established.")
            break
        elif connect_query == 'n': break
        else: print('Please enter a valid response')

    control_opts = {'fancy': fancy_controls, 'text': text_controls}
    while True:
        controls_choice = input('Which type of controlls do you want? (fancy/text): ').lower()
        if controls_choice not in control_opts.keys():
            controls_choice = print('Please enter a valid response')
        else:
            try:
                while True:
                    control_opts[controls_choice]()
            except Exception as e:
                print_tb(e.__traceback__)
                print(f'{type(e).__name__}: {e}')

inter.close()
