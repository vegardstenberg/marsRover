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
import time
from traceback import print_tb
import constants as c

def send_data(bytes_list):
    if connect_query == 'n': return
    bytes_string = ''.join(bytes_list).encode('utf-8')
    print(bytes_string)
    inter.sendall(bytes_string)

def text_controls():
    print("Text controlls activated")

    while True:
        command = input("Available commands: FORWARD, BACKWARD, LEFT, RIGHT. ").lower().split(" ")
        light_sequence = ['0', '0', '0', '0']

        try:
            dir = command[0]
            val = int(command[1])
            end_time = time.time() + val

            while time.time() < end_time:
                if dir in ('forward', 'forwards', 'f', 'w'):
                    light_sequence[0] = '1'
                    print("forward")
                elif dir in ('backward', 'backwards', 'b', 's'):
                    light_sequence[2] = '1'
                    print("backward")
                elif dir in ('right', 'r', 'd'):
                    light_sequence[3] = '1'
                    print("right")
                elif dir in ('left', 'l', 'a'):
                    light_sequence[1] = '1'
                    print("left")
                send_data(light_sequence)

        except KeyboardInterrupt:
            print('Movement aborted')

        except:
            print("Invalid format, please try again.")

def WASD_controlls():
    print("WASD controlls activated.")

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
        screen.fill(c.rgb_black)

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

        text_buttons = ((
            light_index, #Which index in the light string the button corresponds to
            letter, #Which key the button corresponds to
            c.font_arial.render(letter.upper()), #Tuple consisting of a rendered surface of the button's key, and the rect for that surface
            pg.draw.rect( #Draws the button
                screen, #Surface to blit button on
                c.rgb_white, #Button color
                (abs(-(c.button_margin + c.button_size) + light_index * (c.button_margin + c.button_size)) + c.button_margin, #Button margin x-axis
                c.button_margin if light_index == 0 else 2 * c.button_margin + c.button_size, #Button margin y-axis
                c.button_size, #button width
                c.button_size))) #Button height
            for light_index, letter in enumerate('wasd')) #Iterate for the keys "w", "a", "s" and "d"

        for light_index, letter, text, button_rect in text_buttons: #Iterates through every piece of information about each button
            if pg.mouse.get_pressed()[0] and button_rect.collidepoint(pg.mouse.get_pos()): #Checks if lmb pressed and cursor touching the currently iterating button (If this doesn't work, update pygame)
                light_sequence[light_index] = '1' #Marks the corresponding index in the light sequence as on
            if light_sequence[light_index] == '1': #If corresponding index in light sequence is on... (If-statement is neccesary, otherwise button doesn't get highlighted when the corresponding key is pressed instead)
                pg.draw.rect(screen, c.rgb_red, button_rect.inflate(-2 * c.button_margin, -2 * c.button_margin)) #Highlights button with red if it or it's corresponding key is pressed
            text[1].center = button_rect.center #Centers text inside button
            screen.blit(*text) #Blits text (must come after highlight blit, or else text gets covered by it)

        #pg.draw.rect(screen, c.rgb_white, 4 * c.button_margin + 3 * c.button_size, c.button_margin)

        pg.display.flip()

        send_data(light_sequence)

if __name__ == '__main__':
    while True:
        connect_query = input('Want to connect to the rover? (y/n): ').lower()
        if connect_query in ('y', 'yes'):
            connect_query = 'y'
            print("Trying to establish a connection with the rover...")
            try:
                inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                inter.connect((c.pi_ip, 8080))
            except:
                print('Could not connect to the rover. Continuing without connection...')
                connect_query = 'n'
            else: print("Connection established.")
            break
        elif connect_query in ('n', 'no'):
            connect_query = 'n'
            break
        else: print('Please enter a valid response')

    control_opts = {'fancy': fancy_controls, 'text': text_controls}
    while True:
        controls_choice = input('Which type of controlls do you want? (fancy/text): ').lower()
        if controls_choice in control_opts.keys():
            control_opts[controls_choice]()
        else:
            controlls_choice = input("Not a valid choice. Available choices: 'WASD' or 'Text' ")

inter.close()
