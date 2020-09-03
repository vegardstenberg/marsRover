# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:27:40 2020

@author: Vegard Hansen Stenberg
"""

import socket

inter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inter.connect(('192.168.1.147', 8080))
    
inter.sendall(b'10')
inter.close()
