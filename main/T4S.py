import pygame, sys, os
import engine
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
import random
import time

#class auto
#heeft pos(y) bep door origin en hoek



#KLEUREN

black = (0,0,0)
white = (255,255,255)
#draaien

#munten stacey

#noise
class Perlin:
    def __init__(self, frequency):
        if frequency < 2:
            print("Frequency has to be at least 2")
            return
        self.gradients = []
        self.frequency = frequency
        self.lowerBound = 0
        self.interval_size = 100 / (self.frequency-1)
        self.gradients = [random.uniform(-1, 1) for i in range(frequency)]


    def valueAt(self, t):
        if t < self.lowerBound:
            print("Error: Input parameter is out of bounds!")
            return

        discarded = int(self.lowerBound / self.interval_size)

        while t >= (len(self.gradients)-1+discarded)*self.interval_size:
            self.gradients.append(random.uniform(-1, 1))

        numOfintervals = int(t / self.interval_size)
        a1 = self.gradients[numOfintervals-discarded]
        a2 = self.gradients[numOfintervals+1-discarded]

        amt = self.__ease((t-numOfintervals*self.interval_size) / self.interval_size)

        return self.__lerp(a1,a2,amt)

    def discard(self, amount):
        toDiscard = int((amount+self.lowerBound%self.interval_size)/self.interval_size)
        self.gradients = self.gradients[toDiscard:]
        self.lowerBound += amount


    def __ease(self, x):
        return 6*x**5-15*x**4+10*x**3


    def __lerp(self, start, stop, amt):
        return amt*(stop-start)+start



#line class
class Line:
    def __init__(self,index):
        self.index = index
        self.color = black
        #FUNCTIE VOOR HOOGTE
        self.beginy = WINDOW_SIZE[1]/2 + noise.valueAt(index)*WINDOW_SIZE[1]/3
        self.endy = WINDOW_SIZE[1]/2 + noise.valueAt(index+1)*WINDOW_SIZE[1]/3
        self.width = 5

    def draw(self,centerindex):
        self.beginx = WINDOW_SIZE[0]/segments * (self.index + segments/2 - centerindex)
        self.endx = WINDOW_SIZE[0]/segments * (self.index + (segments/2)+1 - centerindex)
        pygame.draw.line(screen,self.color,(self.beginx,self.beginy),(self.endx,self.endy),self.width)

#map maken in lijst terrein

#misc functies
def rot_center(image, angle, x, y):
    '''
    zal een gegeven foto draaien rond center op pos (x,y)
    :param image: foto
    :param angle: hoek om te draaien, pos is tegenwijzerzin
    :param x: x positie
    :param y: y positie
    :return: gedraaide foto, rect waarin foto zich bevindt(kan worden gebruikt om te blitten op scherm)
    '''
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect

#game loop
def game_loop():
    '''
    deze loop is het spel zelf waarnaar verwezen worden wnr op het hoofdmenu op play wordt gedrukt
    :return: /
    '''
    running = True
    #info_label = engine.Label(screen, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), "HIER KOMT SPEL", side = "center")

    latch = 1
    t = 0

    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        t += segments / 400

        # Draw terrain

        for segment in road:
            segment.draw(segments / 2 + t / 5)

            # In en uitladen terrain
            if segment.endx <= 0:
                road.remove(segment)
                road.append(Line(segment.index + segments))

            if segment.beginx >= WINDOW_SIZE[0]:
                road.remove(segment)
                road.append(Line(segment.index - segments))
        #info_label.draw()

        pygame.display.update()

def upgrades_loop():
    '''
    deze loop is het menu waar we upgrades zouden kunnen kopen
    :return: /
    '''
    running = True
    info_label = engine.Label(screen, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), "HIER KOMT UPGRADE MENU", side = "center")
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        info_label.draw()
        pygame.display.update()

def settings_loop():
    '''
    deze loop is een menu voor potentiele instellingen(geluid aan uit)
    :return: /
    '''
    running = True
    info_label = engine.Label(screen, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), "HIER KOMT SETTINGS", side = "center")
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        info_label.draw()
        pygame.display.update()

###window setup (jason) ###
#window setup
pygame.display.set_caption("T4S Game")  #titel venster
window_info = pygame.display.Info() #scherm info ophalen (hoogte/breedte)
#WINDOW_SIZE = (window_info.current_w, window_info.current_h) #hoogte/breedte toekennen
WINDOW_SIZE = (1300,700)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)  # kiezen waar scherm wordt gezet
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), 0, 32) #screen is scherm waar alles op zal worden getekend

### test 
#foto's
logo_img = pygame.image.load("images\T4S_logo.png").convert()
logo_img.set_colorkey((255,255,255))
logo_img = pygame.transform.scale(logo_img, (100,100))
titel_img = pygame.image.load("images\\titel.png").convert()
titel_img.set_colorkey((0,0,0))
titel_img = pygame.transform.scale(titel_img, (1118, 194))
#knoppen
play_button = engine.Button(screen, (50, WINDOW_SIZE[1]-250), "PLAY", font_size=120, transparant=True)
upgrade_button = engine.Button(screen, (play_button.pos[0]+play_button.width+50, WINDOW_SIZE[1]-250), "UPGRADES", font_size=120, transparant=True)
settings_button = engine.Button(screen, (upgrade_button.pos[0]+upgrade_button.width+50, WINDOW_SIZE[1]-250), "SETTINGS", font_size=120, transparant=True)
#parameters
hoek = 0 #hoek waarrond titel wordt gedraaid
sign = 0.25 #dhoek/dt


segments = 50

#Noise klaar zetten
noise = Perlin(500//segments) ## frequentie terrain


#road initialiseren
road = []
i = 0
for segment in range(segments):
    road.append(Line(i))
    i+=1

t = 10





run = True
while run:
    screen.fill((69,69,69))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if play_button.pressed():
                game_loop()
            if upgrade_button.pressed():
                upgrades_loop()
            if settings_button.pressed():
                settings_loop()

    play_button.draw()
    upgrade_button.draw()
    settings_button.draw()
    rotated_titel = rot_center(titel_img, hoek, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 200)
    screen.blit(rotated_titel[0], rotated_titel[1])
    screen.blit(logo_img, (WINDOW_SIZE[0]-110, WINDOW_SIZE[1]-110-30))
    hoek += sign
    if hoek >= 15 or hoek <= 0:
        sign *= -1
    clock.tick(60)
    pygame.display.update()