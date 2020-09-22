# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

import socket
import pygame as pg
inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inter.connect(('192.168.1.59', 8080))

pg.init()
c = pg.time.Clock()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)

while True:
    for event in pg.event.get():
        pass
    c.tick(5)
    key_in = pg.key.get_pressed()
    light_sequence = [0, 0, 0, 0]
    for i in enumerate([pg.K_w, pg.K_a, pg.K_s, pg.K_d]):
        light_sequence[i[0]] = str(key_in[i[1]])
    light_string = ''.join(light_sequence).encode('utf-8')
    inter.sendall(light_string)
    pg.display.flip()

inter.close()
