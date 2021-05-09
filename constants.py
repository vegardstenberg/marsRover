from pygame import freetype as ft
ft.init()

pi_ip = '192.168.1.59'
pg_res = (1280, 720) #Pygame screen resolution
rgb_white = (255, 255, 255)
rgb_black = (0, 0, 0)
rgb_red = (255, 0, 0)

font_size = 70
font_arial = ft.SysFont('Arial', font_size)
b_marg = 10 #Button margin
b_size = 100 #Button size
