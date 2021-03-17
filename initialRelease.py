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
import pgmath as math #Imports the pgmath.py file in this repository, which contains everything from the math.py library, plus some extra pygame math for convenience

class Texture: #Class stolen from some other script I have lol
    #For this class, you can pass the following:
        #tx: image path      #pos: any positional attribute(s) of a rectangle, or a rectangle
        #tx: pygame surface  #pos: any positional attribute(s) of a rectangle, or a rectangle
        #tx: rgb color       #pos: rectangle or rectangle-like tuple
        #tx: Texture class instance (This will return a copy of the passed instance, added for convenience. Can also pass new positional arguments for the copy)
        #Remember to pass rectangles with the "rect"-keyword, and positional attributes with the corresponding attribute name as the keyword
    def __init__(self, tx=c.rgb_black, **pos):
        if type(tx) == self.__class__:
            self.__dict__ = tx.__dict__
            for k, v in pos.items():
                setattr(self.rect, k, v)
            return
        if 'rect' in pos.keys() and type(pos['rect']) == tuple: pos['rect'] = pg.rect(*pos['rect'])
        if type(tx) == tuple:
            self.rect = pos.pop('rect') if 'rect' in pos.keys() else pg.Rect(0, 0, 0, 0)
            for k, v in pos.items():
                setattr(self.rect, k, v)
            self.original_tx = pg.Surface(self.rect.size)
            self.original_tx.fill(tx)
            self.tx.fill(tx)
        else:
            self.original_tx = tx
            self.rect = self.tx.get_rect(center=pos['rect'].center) if 'rect' in pos.keys() else self.tx.get_rect(**pos)
        #Assigning to self.original_tx assigns both original_tx and tx. Use this when you want to replace the texture with a new one
        #Assigning to self.tx assigns just the current tx, and keeps self.original_tx the same. Use this if you wanna modify the current texture (such as rotating it, re-coloring it, etc...)
        #Note: Methods of self.original_tx that changes the object itself (such as .fill) will NOT affect self.tx

    @property
    def original_tx(self):
        return self._original_tx

    @original_tx.setter
    def original_tx(self, tx):
        self._original_tx = tx.convert_alpha() if type(tx) == pg.Surface else pg.image.load(tx).convert_alpha()
        self.tx = self._original_tx.copy()

    def copy(self):
        _copy = self.__class__(topleft=(0, 0))
        _copy.__dict__ = self.__dict__
        return _copy

class Button(Texture):
    #ACCEPTED ARGUMENTS:
        #text (option 1): String, integer, float. This text will be stored as a string (self.text) aswell as a surface (self.text_rendered)
        #text (option 2): image path, pygame surface, rgb color, Texture object. This text will only be stored as a surface (seld.text_rendered)
        #tx: image path, pygame surface, rgb color, Texture object. Anything accepted as tx in the Texture class is also accepted here
        #hold_fill: image path, pygame surface, rgb color, Texture object. Same as tx
        #anchor: The point to align all blittable parts of the button to. Should be a string representing a point on a rectangle
        #on_hold: Callable. This callable will be called every frame the button is held. Anything this callable returns is ignored
        #on_hold_args: Tuple, list. Will be passed as *args into on_hold
        #on_hold_kwargs: Dictionary. Will be passed as **kwargs into on_hold
        #on_click: Callable. This callable will be called once when the button is clicked. Anything this callable returns is ignored
        #on_click_args: Tuple, list. Will be passed as *args into on_click
        #on_click_kwargs: Dictionary. Will be passed as **kwargs into on_click
    def __init__(self, text=None, tx=None, hold_fill=None, anchor='center', on_hold=lambda: None, on_hold_args=(), on_hold_kwargs={}, on_click=lambda: None, on_click_args=(), on_click_kwargs={}, **pos):
        _rect = pg.Rect(0, 0, 0, 0)
        for k, v in pos.items():
            setattr(_rect, k, v)
        anchor = {anchor: math.tupsub(getattr(_rect, anchor), _rect.topleft)}
        if not tx: tx = pg.Surface(_rect.size)
        if type(hold_fill) == tuple: hold_fill = Texture(tx=hold_fill, size=_rect.size)
        super().__init__(tx, **pos)
        self.text = str(text) if type(text) in (str, int, float) else None
        self.text_rendered = Texture(tx=c.font_arial.render(self.text)[0] if self.text else text, **anchor) if text else None
        self.hold_fill = Texture(tx=hold_fill, **anchor) if hold_fill else None
        self.on_hold = on_hold
        self.on_hold_args = on_hold_args
        self.on_hold_kwargs = on_hold_kwargs
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.on_click_kwargs = on_click_kwargs
        self.held = False

    def get_blit(self): #Put together a blittable button and return it
        _blit = self.tx.copy()
        for tx in filter(lambda tx: bool(tx), (self.hold_fill, self.text_rendered)):
            if tx == self.hold_fill and not self.held: continue
            _blit.blit(tx.tx, tx.rect.topleft)
        return _blit

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

    '''

    text_buttons = ((
        light_index, #Which index in the light string the button corresponds to
        letter, #Which key the button corresponds to
        c.font_arial.render(letter.upper()), #Tuple consisting of a rendered surface of the button's key, and the rect for that surface
        pg.draw.rect( #Draws the button
            screen, #Surface to blit button on
            c.rgb_white, #Button color
            (
                abs(-(c.button_margin + c.button_size) + light_index * (c.button_margin + c.button_size)) + c.button_margin, #Button margin x-axis
                c.button_margin if light_index == 0 else 2 * c.button_margin + c.button_size, #Button margin y-axis
                c.button_size, #button width
                c.button_size #Button height
            )
        )
    ) for light_index, letter in enumerate('wasd')) #Iterate for the keys "w", "a", "s" and "d"

    '''

    buttons = {
        letter: Button(
            text=letter.upper(),
            tx=c.rgb_white,
            hold_fill=Texture(tx=c.rgb_red, size=(c.button_size - 2 * c.button_margin,) * 2),
            x=abs(-(c.button_margin + c.button_size) + light_index * (c.button_margin + c.button_size)) + c.button_margin, #Button margin x-axis
            y=c.button_margin if light_index == 0 else 2 * c.button_margin + c.button_size, #Button margin y-axis
            width=c.button_size, #button width
            height=c.button_size #Button height
        )
    for light_index, letter in enumerate('wasd')}

    while True:
        clk.tick(30)
        screen.fill(c.rgb_black)

        for event in pg.event.get():
            if event.type == pg.QUIT: exit() #Kasnskje disconnect fra roveren i stedet for bære sys.exit() her?
            elif joystick and event.type == pg.JOYAXISMOTION and event.axis < 2:
                axis_input[event.axis] = event.value if abs(event.value) > 0.2 else 0
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in filter(lambda button: button.rect.collidepoint(event.pos), buttons.values()):
                    button.on_click(*button.on_click_args, **button.on_click_kwargs)

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

        button_in = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        for button in buttons.values():
            button.held = button.rect.collidepoint(mouse_pos) and button_in[0]
            if button.held:
                button.on_hold(*button.on_click_args, **button.on_click_kwargs)

        pg.draw.rect(screen, c.rgb_white, rect=(4 * c.button_margin + 3 * c.button_size, c.button_margin, 4 * c.button_margin, 2 * c.button_size + c.button_margin), width=c.button_margin)

        screen.blits(blit_sequence=((button.get_blit(), button.rect.topleft) for button in buttons.values()))

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
