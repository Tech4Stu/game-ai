###De indeling van de file zal zijn:   IMPORTS
###                                    ALGEMENE PARAMETERS
###                                    FUNCTIES
###                                    CLASSEN
###                                    GAME LOOP
###                                    DEATH LOOP
###                                    MAIN LOOP
### IMPORTS ###
import time

import pygame, sys, math, os, engine, random
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
from math import sin,cos,tan
#kleuren
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
ground = (135, 86, 16)
lavakleur = (255,100,0)
lavakleur2 = (150, 50, 0)
achtergrond = (50,200,240)
grass = (104, 184, 24)
stone = (130, 126, 121)
segments = 100
scale = 0.02 * segments/50
lavaheight = 500

#Cheats
flat = 0        # een flat world genereren
devmode = 0     #het doodgaan uitschakelen

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

def drawground(road,color):
    road.sort(key=lambda x: x.index,reverse= False)
    group = []
    for stuk in road:
        group.append((stuk.beginx,stuk.beginy))
        group.append((stuk.endx, stuk.endy))
    group.append((WINDOW_SIZE[0],WINDOW_SIZE[1]))
    group.append((0, WINDOW_SIZE[1]))
    pygame.draw.polygon(screen,color,group)

def drawlava():
    '''
    functie om de lava te delen
    '''
    pygame.draw.polygon(screen,lavakleur,((0,WINDOW_SIZE[1]),(0,lavaheight),(WINDOW_SIZE[0],lavaheight),(WINDOW_SIZE[0],WINDOW_SIZE[1])))
    pygame.draw.line(screen,lavakleur2,(0,lavaheight),(WINDOW_SIZE[0],lavaheight),3)

#HOOGTEFUNCTIES
def gety(x):
    '''
    krijg de hoogte van de road op een bepaalde x pos
    :param x: gegeven x positie waarvan hoogte gewenst wordt
    :return: de hoogte op pos x
    '''
    if flat == 0:
        if x < 500:
            return 200
        else:
            return WINDOW_SIZE[1] * 2 / 3 + noise.valueAt(scale * x + 100) * WINDOW_SIZE[1] / 3
    if flat == 1:
        return 300

def getnormal(x):
    y0 = gety(x)
    y1 = gety(x+1)
    hoek = math.atan2(y0-y1,1)
    return hoek + math.pi/2

### CLASSEN ###

class Platform:
    def __init__(self,x):
        self.x = x
        self.breedte = 100
        self.width = 15

    def draw(self,car):
        pygame.draw.line(screen,black,(self.x-self.breedte/2-car.mapx,lavaheight),(self.x+self.breedte/2-car.mapx,lavaheight),self.width)

class Roadsegment:
    def __init__(self,index):
        self.index = index
        self.beginy = gety((WINDOW_SIZE[0] / segments) * (self.index))
        self.endy = gety((WINDOW_SIZE[0] / segments) * (self.index+1))
        self.beginx = WINDOW_SIZE[0] / segments * (self.index)
        self.endx = WINDOW_SIZE[0] / segments * (self.index + 1)

        if self.beginy >= lavaheight or self.endy >= lavaheight:
            self.color = stone
        else:
            self.color = grass
        self.width = 10

    def draw(self,mapx):
        self.beginx = WINDOW_SIZE[0]/segments * (self.index) - mapx
        self.endx = WINDOW_SIZE[0]/segments * (self.index + 1) - mapx
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

        if x2 <= x <= x1 or x1 <= x <= x2:
            a = True

        if x4 <= x <= x3 or x3 <= x <= x4:
            b = True

        if y2 <= y <= y1 or y1 <= y <= y2:
            c = True

        if y4 <= y <= y3 or y3 <= y <= y4:
            d = True

        if a and b and c and d:
            pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 10)
            return (x,y)

class Lava:
    def __init__(self):
        self.pools = [(0,0)]
        self.color = lavakleur2
        self.width = 5
        self.poolthresh = 300   #min afstand voor platform
        self.platforms = []
        self.difframp = 300 #difficulty ramp (hoe snel moeilijker worden)

    def update(self,car):
        i = self.pools[len(self.pools)-1][1]
        self.resolution = 10
        while i <= WINDOW_SIZE[0] + car.mapx:
            if gety(i) >= lavaheight:
                beginx = i
                j = i
                while gety(j) >= lavaheight:
                    j += self.resolution
                endx = j
                self.pools.append((beginx-self.resolution,endx+self.resolution,self.poolthresh))
                i = j
            i += self.resolution

        for pool in self.pools:
            if pool[1] <= car.mapx:
                self.pools.remove(pool)

        if len(self.pools) == 0:
            self.pools = [(0,0,1)]

        self.relativepools = []
        for pool in self.pools:
            self.relativepools.append((pool[0] - car.mapx, pool[1] - car.mapx))

        self.poolthresh = int(car.mapx / self.difframp  + 300)


    def generatePlatforms(self,car):
        self.platforms = []

        for pool in self.pools:
            number = (pool[1] - pool[0]) // pool[2]
            for i in range(number):
                self.platforms.append(Platform((i+1)*(pool[1]-pool[0])/(number+1)+pool[0]))

        for platform in self.platforms:
            platform.draw(car)

class Car:
    def __init__(self, x, y, r):
        self.x = x  #pos op scherm
        self.x_v = 0
        self.x_a = 0
        self.y = y  #pos op scherm
        self.y_v = 0
        self.y_a = 0.02  #Fz
        self.sprong = 2
        self.r = r
        self.color = (0,0,255)
        self.mapx = 0   #
        self.xthresh = 3 #max snelheid
        self.drive = 0.04 #versnelling x
        self.jumping = True
        self.platform = False
        self.rect = pygame.Rect(self.x,self.y,38,102)
        self.player = self.rect

    def draw(self):
        """
        start offset voor rechte foto naar hoek is x= -19, y = -102
        dan moet new_x worden afgetrokken en new_y worden optgeteld
        :return: /
        """
        L = 51  # lengte van halve player rechtstaand in pixels
        a = math.ceil(self.x_v*10)  # hoek van player (rechtstaand is 0° volledig vooruit is -40°)
        if a > self.xthresh*10: # voor de twitch van max en min te vermijden want snelheid kan soms net boven treshhold gaan.
            a = self.xthresh*10
        elif a < -self.xthresh*10+1:
            a = -self.xthresh*10+1
        b = (180-a)/2   # zijn de twee tegenoverstaande hoeken in een gelijkbenige driehoek met a zijnde de derde hoek en beenlengte is L
        c = 90 -b   # is complementaire hoek van b?
        new_x = L*sin(math.radians(a))  # de x pos nodig voor verschuiving van wiel tov rotatie te compenseren
        new_y = new_x*tan(math.radians(c))  # de y pos nodig voor verschuiving van wiel tov rotatie te compenseren
        rot_player = rot_center(player_img, -a, self.x+new_x, self.y+new_y-L)
        #self.player = rot_center(player_img, -a, self.x+new_x, self.y+new_y-L)
        self.player = pygame.Rect(rot_player[1])
        #pygame.draw.rect(screen, (255,1,255), rot_player[1])  #hitbox van gedraaide foto
        screen.blit(rot_player[0], rot_player[1])
    def left(self):
        if self.x_v > -self.xthresh:
            self.x_a = -self.drive
    def right(self):
        if self.x_v < self.xthresh:
            self.x_a = self.drive
    def jump(self):
        if self.jumping == False:
            self.y_v = -self.sprong
            self.jumping = True

    def checkDeath(self):
        if self.y >= lavaheight:
            self.color = red
            return True
        else:
            self.color = (0,0,255)
            return False

    def update(self,lava):
        #het slieren op een helling
        if getnormal(self.mapx + self.x) < math.pi/6 and self.y >= gety(self.mapx+self.x) - 10:
            self.y_v -= sin(getnormal(self.mapx + self.x)) * 0.01
            self.x_v += cos(getnormal(self.mapx + self.x)) * 0.01
        if getnormal(self.mapx + self.x) > math.pi/2 - math.pi/6 and self.y >= gety(self.mapx+self.x) - 10:
            self.y_v -= sin(getnormal(self.mapx + self.x)) * 0.01
            self.x_v += cos(getnormal(self.mapx + self.x)) * 0.01

        self.y_v += self.y_a
        self.y_v *= 0.999
        self.y += self.y_v

        #op de grond?
        if self.y >= gety(self.mapx + self.x):
            self.jumping = False
            self.y = gety(self.mapx + self.x)
        else:
            self.jumping = True

        #op een platform?
        self.platform = False
        for platform in lava.platforms:
            if platform.x - platform.breedte/2 <= self.mapx + self.x <= platform.x + platform.breedte/2 and self.y >= lavaheight - 5:
                self.y = lavaheight - 5
                self.jumping = False
                self.platform = True
        self.x_v += self.x_a
        self.x_v *= 0.99
        self.mapx += self.x_v
        self.x_a = 0
        if self.mapx < 0:
            self.mapx = 0

class Munt:
    def __init__(self,x):
        self.x = x
        self.y = gety(self.x) - 50
        if gety(self.x) > lavaheight:
            self.y = lavaheight - 80
        self.gepakt = False #weten wanneer er een munt is genomen
        self.rect = pygame.Rect(self.x,self.y,20,20) # 20 op 20 is formaat van de munt

    def draw(self,car):
        screen.blit(munten_img, (self.x - car.mapx, self.y))

    def hit(self,car):
        self.rect.x = self.x - car.mapx
        if self.rect.colliderect(car.player):
            self.gepakt = True
            return True
        else:
            return False

class Groep:
    '''
    een class waarin alle munten op het scherm worden getekend, met alsook een var om de punten verzameld aan de hand van munten bij te houden
    '''
    def __init__(self):
        self.munten = []
        self.lastx = 2000
        self.munten.append(Munt(self.lastx))
        self.min = 200
        self.max = 800
        self.volgende = random.randrange(self.min, self.max)
        self.punten = 0

    def update(self,car):
        for munt in self.munten:
            if munt.x < car.mapx:
                self.munten.remove(munt)
        while 1:
            if self.lastx + self.volgende < WINDOW_SIZE[0] + car.mapx:
                self.munten.append(Munt(self.lastx + self.volgende))
                self.lastx += self.volgende
                self.volgende = random.randrange(self.min, self.max)
            else:
                break

    def checkCol(self,car):
        '''
        testen of player een van de munten heeft genomen
        '''
        for munt in self.munten:
            if munt.hit(car):
                self.punten += 200
                self.munten.remove(munt)

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
player_img = pygame.image.load("images\playerV2.png").convert()
player_img.set_colorkey((255,255,255))
player_img = pygame.transform.scale(player_img, (38, 102))
munten_img = pygame.image.load("images/munt2.png").convert()
munten_img.set_colorkey((255,255,255))
munten_img = pygame.transform.scale(munten_img,(20,20))
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
#road initialiseren
noise = Perlin(1000//segments) #frequentie terrain
road = []
i = 0

for segment in range(segments):
    road.append(Roadsegment(i))
    i+=1

### GAME LOOP ###
def game_loop():
    '''
    deze loop is het spel zelf waarnaar verwezen worden wnr op het hoofdmenu op play wordt gedrukt
    :return: /
    '''
    #setup variabelen
    running = True
    score = 0
    score_label = engine.Label(screen, (40, 20), "SCORE: 0", txt_clr = (0,0,0), transparant=True, side="left", txt_side="left")
    car = Car(WINDOW_SIZE[0]/4, -20, 32)
    muntengroep = Groep()
    lava = Lava()
    left = False
    right = False
    jump = False
    #loop
    while running:
        #scherm resetten
        screen.fill(achtergrond)
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
                if event.key == K_UP:
                    jump = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    left = False
                if event.key == K_RIGHT:
                    right = False
                if event.key == K_UP:
                    jump = False
        #terrain regelen
        drawlava()
        lava.update(car)
        lava.generatePlatforms(car)
        drawground(road,ground)
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
        #munten regelen
        muntengroep.update(car)
        muntengroep.checkCol(car)
        for munt in muntengroep.munten:
            munt.draw(car)
        #car regelen
        if right:
            car.right()
        if left:
            car.left()
        if jump:
            car.jump()
        car.update(lava)
        car.draw()
        #death regelen
        if devmode == 0:
            if car.checkDeath():
                running = False
                death_loop(int(score//10))
        #score regelen
        if car.mapx + muntengroep.punten > score:
            score = car.mapx + muntengroep.punten
            score_label.txt = f"SCORE: {int(score//10)}"
        score_label.draw()
        #scherm updaten
        pygame.display.update()

### DEATH LOOP ###
def death_loop(score):
    #setup variabelen
    s = pygame.Surface((WINDOW_SIZE[0],WINDOW_SIZE[1]))
    s.set_alpha(3)
    s.fill((255, 0, 0))
    z = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))
    z.set_alpha(1)
    z.fill((0, 0, 0))
    esc_button = engine.Button(screen, (30, 30),
                                "HOME",
                                width=WINDOW_SIZE[0] // 5,
                                font_size=font_size)
    restart_button = engine.Button(screen, (WINDOW_SIZE[0]/2-WINDOW_SIZE[0]//6, WINDOW_SIZE[1]/2),
                               "RESTART",
                               width=WINDOW_SIZE[0] // 3,
                               font_size=font_size,
                               txt_clr = (255,255,255))
    score_label = engine.Label(screen, (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - restart_button.height),
                               f"SCORE: {score}",
                               side = "center",
                               font_size=font_size,
                               txt_clr=(255,255,255))
    running = True
    i = 0
    #loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if esc_button.pressed():
                    running = False
                if restart_button.pressed():
                    running = False
                    game_loop()

        if i <= 200:
            screen.blit(s, (0, 0))
            i += 1
        else:
            screen.blit(z, (0,0))
            score_label.draw()
            esc_button.draw()
            restart_button.draw()

        pygame.display.update()

### MAIN LOOP ###
titelhoek = 0 #hoek waarrond titel wordt gedraaid
sign = 0.25 #dhoek/dt
main = True
while main:
    screen.fill((69,69,69))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if play_button.pressed():
                game_loop()

    play_button.draw()
    rotated_titel = rot_center(titel_img, titelhoek, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - WINDOW_SIZE[1]//8)
    screen.blit(rotated_titel[0], rotated_titel[1])
    screen.blit(logo_img, (WINDOW_SIZE[0]-logo_img.get_height()*1.1, WINDOW_SIZE[1]-logo_img.get_width()*1.1))
    titelhoek += sign
    if titelhoek >= 15 or titelhoek <= 0:
        sign *= -1
    clock.tick(60)
    pygame.display.update()