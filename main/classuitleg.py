import pygame, sys, engine
from pygame.locals import*
pygame.init()

class Munt:
    def __init__(self):
        pass

    def draw(self):
        pass

#een basic lus om voorbeelden op te testen
run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
