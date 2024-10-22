# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

# ! CAMERA SHIT IS BROKEN FORGOT SHIT STREAM SHIT NEED FIX, I'LL FIX BUT NEED SHIT RASPBERRY SHITT CANERA TRANSFER STREAM INSTEAD; IF RAN IT WOULD USE LAPTOP CAMERA BECAUSE SHIT SHIT IM STUPID

import socket
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame import freetype
from sys import exit
import time
from traceback import print_tb
import constants as c
import camera as cam
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

    def update_rect(self, anchor='center'):
        self.rect = self.original_tx.get_rect(**{anchor: getattr(self.rect, anchor)})

    def round_edges(self, round):
        size = self.rect.size
        _cover = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(_cover, (255, 255, 255), (0, 0, *size), border_radius=round)
        self.tx.blit(_cover, (0, 0), None, pg.BLEND_RGBA_MIN)
        return self

    def copy(self):
        _copy = self.__class__(topleft=(0, 0))
        _copy.__dict__ = {k: v.copy() if hasattr(v, 'copy') else v for k, v in self.__dict__.items()}
        return _copy

class Button(Texture):
    #ACCEPTED ARGUMENTS:
        #text (option 1): String, integer, float. This text will be stored as a string (self.text) aswell as a surface (self.text_rendered)
        #text (option 2): image path, pygame surface, rgb color, Texture object. This text will only be stored as a surface (seld.text_rendered)
        #tx: image path, pygame surface, rgb color, Texture object. Anything accepted as tx in the Texture class is also accepted here
        #hold_fill: image path, pygame surface, rgb color, Texture object. Same as tx
        #key: key attribute of pygame. The key associated with the button
        #anchor: The point to align all blittable parts of the button to. Should be a string representing a point on a rectangle
        #on_hold: Callable. This callable will be called every frame the button is held. Anything this callable returns is ignored
        #on_hold_args: Tuple, list. Will be passed as *args into on_hold
        #on_hold_kwargs: Dictionary. Will be passed as **kwargs into on_hold
        #on_click: Callable. This callable will be called once when the button is clicked. Anything this callable returns is ignored
        #on_click_args: Tuple, list. Will be passed as *args into on_click
        #on_click_kwargs: Dictionary. Will be passed as **kwargs into on_click
    def __init__(self, text=None, tx=None, hold_fill=None, key=None, anchor='center', on_hold=lambda self: None, on_hold_args=(), on_hold_kwargs={}, on_click=lambda self: None, on_click_args=(), on_click_kwargs={}, visible=True, **pos):
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
        self.key = getattr(pg, f'K_{key}')
        self.on_hold = on_hold
        self.on_hold_args = on_hold_args
        self.on_hold_kwargs = on_hold_kwargs
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.on_click_kwargs = on_click_kwargs
        self.held = False
        self.visible = visible

    def copy(self):
        _copy = self.__class__()
        _copy.__dict__ = {k: v.copy() if hasattr(v, 'copy') else v for k, v in self.__dict__.items()}
        return _copy

    def get_blit(self): #Put together a blittable button and return it
        _blit = self.tx.copy()
        for tx in filter(lambda tx: bool(tx), (self.hold_fill, self.text_rendered)):
            if tx == self.hold_fill and not self.held: continue
            _blit.blit(tx.tx, tx.rect.topleft)
        return _blit

    def round_edges(self, round):
        super().round_edges(round)


class Slider(Texture): # carbonara
    def __init__(self, valrange, default_value, increment, poskeys, negkeys, border=c.b_marg, border_color=(255, 255, 255), bg_color=(0, 0, 0), slider_tx={'tx': 'textures/gradient.png'}, horizontal=False, reverse=False, size_includes_border=False, visible=True, **pos):
        if valrange[1] - valrange[0] < 0:
            reverse = not reverse
            valrange = tuple(reversed(valrange))
        if size_includes_border:
            border_tx = Texture(tx=border_color, **pos)
            bg_tx = Texture(tx=bg_color, rect=border_tx.rect.inflate(*(border * -2,) * 2))
        else:
            bg_tx = Texture(tx=bg_color, **pos)
            border_tx = Texture(tx=border_color, rect=bg_tx.rect.inflate(*(border * 2) * 2))
        border_tx.original_tx.blit(bg_tx.tx, (border,) * 2)
        border_tx.tx = border_tx.original_tx
        super().__init__(tx=border_tx.tx, rect=border_tx.rect)
        self.valrange = valrange
        self.value = default_value
        self.increment = increment
        self.horizontal = horizontal
        self.reverse = reverse
        self.keys = {k: v if type(v) in (list, tuple) else (v,) for k, v in (('pos', poskeys), ('neg', negkeys))}
        self.visible = visible

        self.slider = Texture(**slider_tx, topright=(self.rect.w - border, border)) # bolognese
        if horizontal: self.slider.original_tx = pg.transform.rotate(self.slider.original_tx, -90)
        self.reverse_slider = self.slider.copy()
        flipped_slider = getattr(self, 'slider' if reverse else 'reverse_slider')
        flipped_slider.original_tx = pg.transform.flip(flipped_slider.original_tx, horizontal, not horizontal)
        flipped_slider.rect.bottomleft = (border, self.rect.h - border)
        if max(valrange) - min(valrange) != 0:
            length_scale_pos = len(range(min(valrange) if min(valrange) > 0 else 0, max(valrange))) / (max(valrange) - min(valrange))
            length_scale_neg = len(range(min(valrange), max(valrange) if max(valrange) < 0 else 0)) / (max(valrange) - min(valrange))
        else: length_scale_pos = length_scale_neg = 0
        if horizontal:
            self.slider.original_tx = pg.transform.scale(self.slider.original_tx, (round(bg_tx.rect.w * length_scale_pos), bg_tx.rect.h))
            self.reverse_slider.original_tx = pg.transform.scale(self.reverse_slider.original_tx, (round(bg_tx.rect.w * length_scale_neg), bg_tx.rect.h))
        else:
            self.slider.original_tx = pg.transform.scale(self.slider.original_tx, (bg_tx.rect.w, round(bg_tx.rect.h * length_scale_pos)))
            self.reverse_slider.original_tx = pg.transform.scale(self.reverse_slider.original_tx, (bg_tx.rect.w, round(bg_tx.rect.h * length_scale_neg)))
        self.slider.update_rect(anchor='bottomleft' if reverse else 'topright')
        self.reverse_slider.update_rect(anchor='topright' if reverse else 'bottomleft')

        # https://upload.wikimedia.org/wikipedia/commons/7/73/Mama_instant_noodle_block.jpg

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        if newval < self.valrange[0]: self._value = self.valrange[0]
        elif newval > self.valrange[1]: self._value = self.valrange[1]
        else: self._value = newval

    def copy(self):
        _copy = self.__class__(valrange=(0, 0), default_value=0, increment=0, poskeys=(), negkeys=())
        _copy.__dict__ = {k: v.copy() if hasattr(v, 'copy') else v for k, v in self.__dict__.items()}
        return _copy

    def get_blit(self): # I'm pretty sure this makes the fancy buttons animated (i think)
        _blit = self.tx.copy()
        if self.value != 0:
            if self.value > 0:
                slider = self.slider
                length = self.value / (max(self.valrange) - min(self.valrange) if min(self.valrange) > 0 else max(self.valrange))
            else:
                slider = self.reverse_slider
                length = self.value / (min(self.valrange) + max(self.valrange) if max(self.valrange) < 0 else min(self.valrange))
            if self.horizontal:
                length = round(slider.rect.w * length)
                if (self.value > 0) is self.reverse: _blit.blit(slider.tx, (slider.rect.left + (slider.rect.w - length), slider.rect.top), area=(slider.rect.w - length, 0, length, slider.rect.h))
                else: _blit.blit(slider.tx, slider.rect.topleft, area=(0, 0, length, slider.rect.h))
            else:
                length = round(slider.rect.h * length)
                if (self.value > 0) is self.reverse: _blit.blit(slider.tx, slider.rect.topleft, area=(0, 0, slider.rect.w, length))
                else: _blit.blit(slider.tx, (slider.rect.left, slider.rect.top + (slider.rect.h - length)), area=(0, slider.rect.h - length, slider.rect.w, length))
        return _blit

def send_data(bitlist, is_string=False): # function that sends a bitstring to the rover
    if not is_string: bitstring = ''.join(bitlist)
    # print("test")
    # print(bitstring)
    bitstring = f'&{bitstring}&'.encode('utf-8')
    # print(bitstring)
    if connect_query == 'y':
        inter.sendall(bitstring)

def text_controls(): # prints the "available" commands and feeds your input into send_data()
    print('Text controlls activated')
    command_list = ('help', 'drive', 'reverse', 'turn right', 'turn left', 'set speed', 'get_speed', 'set turnspeed', 'get_turn', 'steer left', 'steer right', 'stop')
    while True:
        print('------------------------------------------------------------------')
        print('Available commands: \n HELP, DRIVE, REVERSE, TURN LEFT, STEER LEFT, \n TURN RIGHT, STEER RIGHT, SET SPEED, SET TURNSPEED')
        print('------------------------------------------------------------------')
        commands = input('Enter a command (to enter multiple, separate them using "|"):  ').lower()
        if commands.strip(' ').lower() == "help":
            print('------------------------------------------------------------------')
            print("To use the rover you need to provide certain values \n To provide these you write '-' and what you want to provide \n Available values: \n '-s' // Speed \n '-d' // Duration \n '-t' // Turning Speed \n '-r' // Turning Radius")
            print("Example: drive -d 30 -s 126")
            print('------------------------------------------------------------------')
        else:
            send_data(f'1{commands}')

def fancy_controls(): # faNcY
    print("Fancy controlls activated.")

    pg.init()
    clk = pg.time.Clock()
    screen = pg.display.set_mode(c.pg_res, pg.RESIZABLE)
    try: joystick = pg.joystick.Joystick(0)
    except pg.error: joystick = None
    else: joystick.init()

    axis_input = [0, 0]
    bitlist = ['0',] + ('0 ' * 4).split() + ('1 ' * 16).split()
    speed = 256

    def button_hold_func(self, seq):
        seq['wasd'.index(self.text.lower()) + 1] = '1'

    buttons = {
        letter: Button(
            text=letter.upper(),
            tx=c.rgb_white,
            hold_fill=Texture(tx=c.rgb_red, size=(c.b_size - 2 * c.b_marg,) * 2),
            key=letter,
            on_hold=button_hold_func,
            on_hold_args=(bitlist,),
            x=abs(-(c.b_marg + c.b_size) + light_index * (c.b_marg + c.b_size)) + c.b_marg, #Button margin x-axis
            y=c.b_marg if light_index == 0 else 2 * c.b_marg + c.b_size, #Button margin y-axis
            width=c.b_size, #button width
            height=c.b_size #Button height
        )
    for light_index, letter in enumerate('wasd')}

    sliders = {
        'speed': Slider(
            valrange=(0, 126),
            default_value=126,
            increment=1,
            poskeys=pg.K_UP,
            negkeys=pg.K_DOWN,
            size_includes_border=True,
            size=(c.b_size, c.pg_res[1] - c.b_size - 3 * c.b_marg),
            topright=(c.pg_res[0] - c.b_marg, c.b_marg)
        ),
        'keyboard_steering': Slider(
            valrange=(0, 126),
            default_value=126,
            increment=1,
            poskeys=pg.K_RIGHT,
            negkeys=pg.K_LEFT,
            horizontal=True,
            size_includes_border=True,
            size=(c.pg_res[0] - c.b_size - 3 * c.b_marg, c.b_size),
            bottomleft=(c.b_marg, c.pg_res[1] - c.b_marg),
        ),
        'controller_steering': Slider(
            valrange=(-126, 126),
            default_value=0,
            increment=2,
            poskeys=pg.K_RIGHT,
            negkeys=pg.K_LEFT,
            horizontal=True,
            size_includes_border=True,
            size=(c.pg_res[0] - c.b_size - 3 * c.b_marg, c.b_size),
            bottomleft=(c.b_marg, c.pg_res[1] - c.b_marg),
            visible=False
        )
    }

    while True:
        clk.tick(30)
        screen.fill(c.rgb_black)
        cam_frame = cam.get_frame()
        screen.blit(cam_frame, dest=buttons['a'].rect.bottomleft)

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                inter.close()
                exit() #Kasnskje disconnect fra roveren i stedet for bære sys.exit() her? --- Nææææh, mvh ic1cle
            elif joystick and event.type == pg.JOYAXISMOTION and event.axis < 2:
                axis_input[event.axis] = event.value if abs(event.value) > 0.2 else 0
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in filter(lambda button: button.rect.collidepoint(event.pos), buttons.values()):
                    button.on_click(button, *button.on_click_args, **button.on_click_kwargs)

        for i in range(1, 5):
            bitlist[i] = '0'

        if joystick:
            if axis_input[0] < 0:
                bitlist[2] = '1'
            elif axis_input[0] > 0:
                bitlist[4] = '1'
            if axis_input[1] < 0:
                bitlist[1] = '1'
            elif axis_input[1] > 0:
                bitlist[3] = '1'

        key_in = pg.key.get_pressed()

        for slider in filter(lambda s: s.visible, sliders.values()):
            if any(key_in[key] for key in slider.keys['pos']): slider.value += slider.increment
            elif any(key_in[key] for key in slider.keys['neg']): slider.value -= slider.increment

        for i in ((2, pg.K_UP), (-2, pg.K_DOWN)):
            if key_in[i[1]] and 0 <= speed + i[0] <= 256: speed += i[0]
            binaryspeed = '{0:08b}'.format(speed - 1)
            for i in range(8):
                bitlist[5 + i] = binaryspeed[i]

        binaryspeed = '{0:08b}'.format(sliders['speed'].value)
        for i in range(8):
            bitlist[5 + i] = binaryspeed[i]

        binarysteering = '{0:08b}'.format(sliders['keyboard_steering'].value)
        for i in range(8):
            bitlist[13 + i] = binarysteering[i]

        button_in = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        for button in buttons.values():
            button.held = (button.rect.collidepoint(mouse_pos) and button_in[0]) or key_in[button.key]
            if button.held:
                button.on_hold(button, *button.on_hold_args, **button.on_hold_kwargs)

        screen.blits(blit_sequence=(
            *((button.get_blit(), button.rect.topleft) for button in filter(lambda b: b.visible, buttons.values())),
            *((slider.get_blit(), slider.rect.topleft) for slider in filter(lambda s: s.visible, sliders.values())),
        ))

        pg.display.flip()

        send_data(bitlist)

if __name__ == '__main__':
    while True:
        connect_query = input('Want to connect to the rover? (y/n) [+ip]: ').lower().split()
        if len(connect_query) == 1:
            ip = c.pi_ip
            connect_query = connect_query[0]
        elif len(connect_query) == 2:
            ip = connect_query[1]
            connect_query = connect_query[0]
        else: connect_query = ''
        if connect_query in ('y', 'yes'):
            connect_query = 'y'
            print('Trying to establish a connection with the rover...')
            try: # tries to connect the socket to the rover
                inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                inter.connect((ip, 8080))
            except:
                print('Could not connect to the rover. Continuing without connection...')
                connect_query = 'n'
            else: print('Connection established')
            break
        elif connect_query in ('n', 'no'):
            connect_query = 'n'
            break
        else: print('Please enter a valid response')

    control_opts = {'': fancy_controls, 'text': text_controls}
    controls_choice = input('Do you want text controls? (y/n): ').lower()
    while True:
        if controls_choice in ('y', 'yes'):
            text_controls()
        elif controls_choice in ('n', 'no'):
            fancy_controls()
        else:
            controls_choice = input('Please enter a valid response (y/n): ')

inter.close()
