###De indeling van de file zal zijn:   IMPORTS
###                                    FUNCTIES
###                                    CLASSEN
###                                    ALGEMENE PARAMETERS
###                                    GAME LOOP
###                                    UPGRADES LOOP
###                                    SETTINGS LOOP
###                                    MAIN LOOP
### IMPORTS ###
import pygame, sys, math, os, engine, random
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
from math import sin
#kleuren
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

### FUNCTIES ###
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

### CLASSEN ###
class Roadsegment:
    def __init__(self,index, flat=False):
        self.index = index
        self.color = black
        #FUNCTIE VOOR HOOGTE
        if flat:
            self.beginy = WINDOW_SIZE[1]-100
            self.endy = WINDOW_SIZE[1]-100
        else:
            self.beginy = WINDOW_SIZE[1]/2 + noise.valueAt(index)*WINDOW_SIZE[1]/3
            self.endy = WINDOW_SIZE[1]/2 + noise.valueAt(index+1)*WINDOW_SIZE[1]/3
        self.width = 5

    def draw(self,mapx):
        self.beginx = WINDOW_SIZE[0]/segments * (self.index - mapx/segments)
        self.endx = WINDOW_SIZE[0]/segments * (self.index + 1 - mapx/segments)
        pygame.draw.line(screen,self.color,(self.beginx,self.beginy),(self.endx,self.endy),self.width)

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

class Line:
    def __init__(self,beginx,beginy,endx,endy):
        self.beginx = beginx
        self.beginy = beginy
        self.endx = endx
        self.endy = endy
        self.width = 5
        self.color = red

    def draw(self):
        pygame.draw.line(screen, self.color, (self.beginx, self.beginy), (self.endx, self.endy), self.width)

    def collide(self,line):
        x1 = self.beginx
        x2 = self.endx
        x3 = line.beginx
        x4 = line.endx
        y1 = self.beginy
        y2 = self.endy
        y3 = line.beginy
        y4 = line.endy

        div = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        x = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/div
        y = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/div

        a = False
        b = False
        c = False
        d = False

        if x1 >= x2:
            if x2 <= x and x <= x1:
                a = True
        else:
            if x1 <= x and x <= x2:
                a = True

        if x3 >= x4:
            if x4 <= x and x <= x3:
                b = True
        else:
            if x3 <= x and x <= x4:
                b = True

        if y1 >= y2:
            if y2 <= y and y <= y1:
                c = True
        else:
            if y1 <= y and y <= y2:
                c = True

        if y3 >= y4:
            if y4 <= y and y <= y3:
                d = True
        else:
            if y3 <= y and y <= y4:
                d = True
        if a and b and c and d:
            pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 10)
            return (x,y)

class Car:
    def __init__(self, x, y, r):
        self.x = x
        self.x_v = 0
        self.x_a = 0
        self.y = y
        self.y_v = 0
        self.y_a = 0
        self.r = r
        self.color = (0,0,255)
        self.mapx = 0
        self.xthresh = 0.5
        self.drive = 0.1

    def draw(self):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.r)

    def left(self):
        if self.x_a <= self.xthresh:
            self.x_a = -self.drive
    def right(self):
        if self.x_a <= self.xthresh:
            self.x_a = self.drive

    def update(self):
        #somF = m*a -> x_a = Fx/m  // y_a = Fy/m
        if self.y >= gety(self.mapx / 2 + self.x):
            self.y = gety(self.mapx / 2 + self.x)
        else:
            self.y_a = 0.01
            self.y_v += self.y_a
            self.y_v *= 0.999
            self.y += self.y_v
            self.y_a = 0

        self.x_v += self.x_a
        self.x_v *= 0.99
        self.mapx += self.x_v
        self.x_a = 0

### ALGEMENE PARAMETERS ###
# window setup
pygame.display.set_caption("T4S Game")  # titel venster
WINDOW_SIZE = (1300,700)    # venster grootte
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 200)  # kiezen waar scherm wordt gezet
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), 0, 32) # screen is scherm waar alles op zal worden getekend
# foto's inladen
logo_img = pygame.image.load("images\T4S_logo.png").convert()
logo_img.set_colorkey((255,255,255))
logo_img = pygame.transform.scale(logo_img, (50,50)) # x5
titel_img = pygame.image.load("images\hillclimber_logo.png").convert()
titel_img.set_colorkey((255,255,255))
titel_img = pygame.transform.scale(titel_img, (839, 146)) # x1.5
# knoppen
font_size = 90
spacing = 30
button_height = engine.Label(screen, (0,0), "", font_size= font_size).height + spacing
play_button = engine.Button(screen,
                            (spacing, WINDOW_SIZE[1]-button_height),
                            "PLAY",
                            width = WINDOW_SIZE[0]//6,
                            font_size=font_size,
                            transparant=True)
upgrade_button = engine.Button(screen,
                            (play_button.pos[0]+play_button.width+spacing, WINDOW_SIZE[1]-button_height),
                            "UPGRADES",
                            width = WINDOW_SIZE[0]//3,
                            font_size=font_size,
                            transparant=True)
settings_button = engine.Button(screen,
                            (upgrade_button.pos[0]+upgrade_button.width+spacing, WINDOW_SIZE[1]-button_height),
                            "SETTINGS",
                            width = WINDOW_SIZE[0]//3,
                            font_size=font_size,
                            transparant=True)
#road initialiseren
segments = 50
noise = Perlin(500//segments) #frequentie terrain
road = []
i = 0
for segment in range(segments):
    road.append(Roadsegment(i))
    i+=1
# rest
titelhoek = 0 #hoek waarrond titel wordt gedraaid
sign = 0.25 #dhoek/dt
main = True

def gety(x):
    return WINDOW_SIZE[1] / 2 + noise.valueAt(x * segments / WINDOW_SIZE[0] ) * WINDOW_SIZE[1] / 3

### GAME LOOP ###
def game_loop():
    '''
    deze loop is het spel zelf waarnaar verwezen worden wnr op het hoofdmenu op play wordt gedrukt
    :return: /
    '''
    car = Car(100, -20, 10) #gwn nog zodat game menu werkt, moet nog veranderd worden
    left = False
    right = False
    running = True
    t = 0
    while running:
        #scherm resetten
        screen.fill((255,255,255))
        #events handelen
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT:
                    left = True
                if event.key == K_RIGHT:
                    right = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    left = False
                if event.key == K_RIGHT:
                    right = False
        # Draw terrain
        for segment in road:
            # In en uitladen terrain
            segment.draw(car.mapx)
            if segment.endx <= 0:
                new = Roadsegment(segment.index + segments)
                road.remove(segment)
                road.append(new)
                new.draw(car.mapx)
            if segment.beginx >= WINDOW_SIZE[0]:
                new = Roadsegment(segment.index - segments)
                road.remove(segment)
                new.draw(car.mapx)
                road.append(new)

        # keyinputs handelen
        if right:
            car.right()
        if left:
            car.left()

        car.update()
        car.draw()
        #pygame.draw.circle(screen,black,(WINDOW_SIZE[0]/2*sin(t)+WINDOW_SIZE[0]/2,gety(WINDOW_SIZE[0]/2*sin(t)+WINDOW_SIZE[0]/2)),10)

        pygame.display.update()
        t += 0.01
### UPGRADES LOOP ###
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

### SETTINGS LOOP ###
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

### MAIN LOOP ###
while main:
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
    rotated_titel = rot_center(titel_img, titelhoek, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - WINDOW_SIZE[1]//8)
    screen.blit(rotated_titel[0], rotated_titel[1])
    screen.blit(logo_img, (WINDOW_SIZE[0]-logo_img.get_height()*1.1, WINDOW_SIZE[1]-logo_img.get_width()*1.1))
    titelhoek += sign
    if titelhoek >= 15 or titelhoek <= 0:
        sign *= -1
    clock.tick(60)
    pygame.display.update()