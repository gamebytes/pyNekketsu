#! /usr/bin/python


import pygame
import os


import sys
sys.path.insert(0, "engine")

from displayzoom import DisplayZoom
from match import Match

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

dz=DisplayZoom(3,"pyNekketsu",256, 240)
match=Match()

while 1:
    if (match.player1.inputs.Esc):#pb: what to do if no player1 in game ?
        pygame.quit()
        sys.exit()

    match.update()

    match.draw(dz.surface)
    dz.update()
    mainClock.tick(40)
    
