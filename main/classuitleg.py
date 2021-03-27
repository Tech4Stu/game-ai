import pygame, sys, engine
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()

class Voorbeeld:
    def __init__(self, x, y, kleur, breedte):
        self.x = x
        self.y = y
        self.kleur = kleur
        self.breedte = breedte

    def draw(self, surface):
        pygame.draw.rect(surface, self.kleur, (self.x, self.y, self.breedte, self.breedte))
        pygame.display.update()

class Munt:
    def __init__(self, x):
        self.x = x
        self.gepakt = False
        self.rect = pygame.Rect(x, 100, 50,50)
        self.kleur = (100,100,0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.kleur, self.rect)
        pygame.display.update()
    def collision(self, x, y):
        if self.rect.collidepoint(x, y):
            self.kleur = (0,100,100)
        else:
            self.kleur = (100,100,0)
    def score(self):


#een basic lus om voorbeelden op te testen
run = True
vb1 = Voorbeeld(50,50, (255,0,0), 5)
vb2 = Voorbeeld(200, 300, (0,255,0), 10)
munt = Munt(200)
screen = pygame.display.set_mode((500,500))
while run:
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    vb1.draw(screen)
    vb2.draw(screen)
    munt.draw(screen)
    mouse_pos = pygame.mouse.get_pos()
    munt.collision(mouse_pos[0], mouse_pos[1])
    print(munt.kleur, mouse_pos)
    clock.tick(60)
