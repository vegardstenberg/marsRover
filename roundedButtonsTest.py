# Importing the library
import pygame
 
pygame.init()
surface = pygame.display.set_mode((400, 300))
color = (48, 141, 70)
 
while True:
    pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60),  2, 3)
    pygame.display.flip()