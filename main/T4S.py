import pygame, sys, os, math
import engine
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
import random

class krachten:
    def __init__(self, F, hoek, x_dist, y_dist):
        '''
        zal gegeven kracht omzetten in kracht in center en het bijhorende moment
        :param F: grootte
        :param hoek: is de hoek van de krachtenpijl
        :param x_dist: loodrechte afstand van center naar Y kracht  (C->Y)
        :param y_dist: loodrechte afstand van center naar X kracht  (C->X)
        '''
        self.F = F
        self.hoek = hoek
        self.x_dist = x_dist
        self.y_dist = y_dist
        self.__Fx = self.F*math.cos(self.hoek)
        self.__Fy = self.F*math.sin(self.hoek)
        self.__M = self.__Fy*abs(self.x_dist) + self.__Fx*abs(self.y_dist)   #pos is tegenklok

        #return self.Fx, self.Fy, self.M
    def get_Fx(self):
        return self.__Fx

    def get_Fy(self):
        return self.__Fy

    def get_M(self):
        return self.__M

    def get_all(self):
        return self.__Fx, self.__Fy, self.__M

    def set_Fx(self, Fx):
        self.__Fx = Fx

    def set_Fy(self, Fy):
        self.__Fy = Fy

    def set_M(self, M):
        self.__M = M

    def set_all(self, Fx, Fy, M):
        self.__Fx = Fx
        self.__Fy = Fy
        self.__M  = M

    def __add__(self, other):
        added_Fx = self.get_Fx() + other.get_Fx()
        added_Fy = self.get_Fy() + other.get_Fy()
        added_M  = self.get_M() + other.get_M()
        result = krachten(0,0,0,0)
        result.set_all(added_Fx, added_Fy, added_M)
        return result


class Car:
    def __init__(self, x, y, width, height, mass):
        self.centerx = x
        self.centery = y
        self.width = width
        self.height = height
        self.mass = mass
        #krachten (snelheid, versnelling)
        self.x_v = 0
        self.y_v = 0
        self.x_a = 0
        self.y_a = 0
        self.I = self.width * self.height * self.height * self.height / 12 #traagheidsmoment bh³/12
        self.hoek = 0 #radialen
        self.omega = 0
        self.alpha = 0
        #hoekpunten bepalen
        self.L = math.sqrt((self.height*self.height+self.width*self.width)/4) #lengte van center -> hoekpunten
        self.hoekpunthoek = math.atan2(self.height, self.width) #geeft hoek van center -> hoekpunten atan2 == atan(y/x)
        #de vier lijnen voor collision
        self.Lline = Line(1)    #left line
        self.Rline = Line(1)    #right line
        self.Tline = Line(1)    #top line
        self.Bline = Line(1)    #bottom line

    def draw(self):
        alpha1 = math.pi - self.hoekpunthoek + self.hoek
        alpha2 = self.hoekpunthoek + self.hoek
        alpha3 = -self.hoekpunthoek + self.hoek
        alpha4 = math.pi + self.hoekpunthoek + self.hoek
        x1 = self.L * math.cos(alpha1) + self.centerx
        y1 = self.L * math.sin(alpha1) + self.centery
        x2 = self.L * math.cos(alpha2) + self.centerx
        y2 = self.L * math.sin(alpha2) + self.centery
        x3 = self.L * math.cos(alpha3) + self.centerx
        y3 = self.L * math.sin(alpha3) + self.centery
        x4 = self.L * math.cos(alpha4) + self.centerx
        y4 = self.L * math.sin(alpha4) + self.centery
        pygame.draw.polygon(screen, red, ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 3)


    def update(self, krachtenlijst):
        '''
        krijgt een lijst binnen van alle werkende krachten op auto en veranderd x,y,v,a,... volgens deze krachten
        :param krachten: krachten lijst , zijnde Fz, Fgas, Frem, Fcoll, (Fvering)
        :return: /
        '''
        total_F = krachten(0,0,0,0) #is een object krachten() die de som van alle ingegeven/inwerkende krachten op de auto
        for kracht in krachtenlijst:
            total_F += kracht
        print(total_F.get_all())
        #somF = m*a -> x_a = Fx/m  // y_a = Fy/m
        self.x_a = total_F.get_Fx()/self.mass
        self.x_v = 1
        self.centerx = 1
        self.y_a = total_F.get_Fy()/self.mass
        self.y_v = 1
        self.centery = 1
        #somM = I*alpha
        self.alpha = total_F.get_M()/self.I
        self.omega = 1
        self.hoek = 1

#KLEUREN
black   = (0,0,0)
white   = (255,255,255)
red     = (255,0,0)

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

        kleinste = x1
        grootste = x2

        if x1 > x2:
            grootste = x1
            kleinste = x2

        if kleinste < x < grootste:
            a = True

        if x3 > x4:
            if x4 < x and x < x3:
                b = True
        else:
            if x3 < x and x < x4:
                b = True

        if y1 > y2:
            if y2 < y and y < y1:
                c = True
        else:
            if y1 < y and y < y2:
                c = True

        if y3 > y4:
            if y4 < y and y < y3:
                d = True
        else:
            if y3 < y and y < y4:
                d = True

        if a and b and c and d:
            pygame.draw.circle(gameDisplay, (255, 0, 0), (x, y), 10)

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
    latch = 1
    t = 0
    car = Car(WINDOW_SIZE[0]//4, 100, 100, 50, 5)
    g = 9.81
    Fz = krachten(car.mass*g, -math.pi/2, 0, 0)                 #zwaartekracht m*g
    Fgas = krachten(100, 0, -car.width/2, -car.height/2)        #gaskracht waarde kan bepaald worden nu gwn 100
    Frem = krachten(100, math.pi, -car.width/2, -car.height/2)  #remkracht idem
    Fcoll = krachten(0,0,0,0)                                   #collision kracht
    left = False
    right = False
    running = True
    while running:
        #scherm resetten
        screen.fill(white)
        krachtenlijst = []
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
        # keyinputs handelen
        if left:
            krachtenlijst.append(Frem)
        if right:
            krachtenlijst.append(Fgas)
        # Draw terrain
        t += segments / 400
        for segment in road:
            segment.draw(segments / 2 + t / 5)
            # In en uitladen terrain
            if segment.endx <= 0:
                road.remove(segment)
                road.append(Line(segment.index + segments))
            if segment.beginx >= WINDOW_SIZE[0]:
                road.remove(segment)
                road.append(Line(segment.index - segments))
        #auto handelen
        krachtenlijst.append(Fz)
        krachtenlijst.append(Fcoll)

        car.update(krachtenlijst)
        car.draw()



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

#window setup
pygame.display.set_caption("T4S Game")  #titel venster
#window_info = pygame.display.Info() #scherm info ophalen (hoogte/breedte)
#WINDOW_SIZE = (window_info.current_w, window_info.current_h) #hoogte/breedte toekennen
WINDOW_SIZE = (1300,700)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 200)  # kiezen waar scherm wordt gezet
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), 0, 32) #screen is scherm waar alles op zal worden getekend
#foto's
logo_img = pygame.image.load("images\T4S_logo.png").convert()
logo_img.set_colorkey((255,255,255))
logo_img = pygame.transform.scale(logo_img, (50,50)) #x5
titel_img = pygame.image.load("images\\titel.png").convert()
titel_img.set_colorkey((0,0,0))
titel_img = pygame.transform.scale(titel_img, (839, 146)) #x1.5
#knoppen
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
    rotated_titel = rot_center(titel_img, hoek, WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - WINDOW_SIZE[1]//8)
    screen.blit(rotated_titel[0], rotated_titel[1])
    screen.blit(logo_img, (WINDOW_SIZE[0]-logo_img.get_height()*1.1, WINDOW_SIZE[1]-logo_img.get_width()*1.1))
    hoek += sign
    if hoek >= 15 or hoek <= 0:
        sign *= -1
    clock.tick(60)
    pygame.display.update()