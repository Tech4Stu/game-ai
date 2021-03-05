import pygame, sys, os, math
import engine
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
import random


def reactie(punten,car):
    if len(punten) == 2 and punten[0] != punten[1]:
        hoek = float(math.atan2(punten[1][1]-punten[0][1],punten[0][0]-punten[1][0]))
        corr_hoek = hoek - math.pi/2
        kracht = 1
        
        return [kracht, corr_hoek, (punten[0][0] + punten[1][0]) / 2 - car.centerx,
                (punten[1][1] + punten[0][1]) / 2 - car.centery]
    else:
        print("meer dan 2 punten")
        quit()
        return 5

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
        self.update()

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

    def set_pos(self, x, y):
        self.x_dist = x
        self.y_dist = y
        self.update()

    def __add__(self, other):
        added_Fx = self.get_Fx() + other.get_Fx()
        added_Fy = self.get_Fy() + other.get_Fy()
        added_M  = self.get_M() + other.get_M()
        result = krachten(0,0,0,0)
        result.set_all(added_Fx, added_Fy, added_M)
        return result

    def draw(self,car, color=(0,0,0)):
        pygame.draw.line(screen,color,(car.centerx+self.x_dist,car.centery+self.y_dist),(car.centerx+self.x_dist+self.__Fx*1000,car.centery+self.y_dist+self.__Fy*1000),5)

    def update(self):
        '''
        update was nodig om alle krachten te herberekenen wnr x/y wordt veranderd
        :return: /
        '''
        self.__Fx = self.F * math.cos(self.hoek)
        self.__Fy = -self.F * math.sin(self.hoek)
        self.__M = self.__Fy * abs(self.x_dist) + self.__Fx * abs(self.y_dist)  # pos is tegenklok

class Car:
    def __init__(self, x, y, width, height, mass):
        self.mapx = 0
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
        self.hoek = 0.05 #radialen
        self.omega = 0
        self.alpha = 0
        #hoekpunten bepalen
        self.L = math.sqrt((self.height*self.height+self.width*self.width)/4) #lengte van center -> hoekpunten /diagonaal
        self.hoekpunthoek = math.atan(self.height/self.width) #geeft hoek van center -> hoekpunten atan2 == atan(y/x)
        #de vier lijnen voor collision
        self.calculate_pos()
        self.collisionbox = []
        self.collisionbox.append(Line(self.x1, self.y1, self.x2, self.y2))
        self.collisionbox.append(Line(self.x2, self.y2, self.x3, self.y3))
        self.collisionbox.append(Line(self.x3, self.y3, self.x4, self.y4))
        self.collisionbox.append(Line(self.x4, self.y4, self.x1, self.y1))

    def draw(self):
        self.collisionbox = []
        self.collisionbox.append(Line(self.x1, self.y1, self.x2, self.y2))
        self.collisionbox.append(Line(self.x2, self.y2, self.x3, self.y3))
        self.collisionbox.append(Line(self.x3, self.y3, self.x4, self.y4))
        self.collisionbox.append(Line(self.x4, self.y4, self.x1, self.y1))
        pygame.draw.circle(screen, red, (int(self.x1), int(self.y1)), 10)
        for line in self.collisionbox:
            line.draw()

    def calculate_pos(self):
        alpha1 = math.pi - self.hoekpunthoek + self.hoek
        alpha2 = self.hoekpunthoek + self.hoek
        alpha3 = -self.hoekpunthoek + self.hoek
        alpha4 = math.pi + self.hoekpunthoek + self.hoek
        self.x1 = self.L * math.cos(alpha1) + self.centerx
        self.y1 = -self.L * math.sin(alpha1) + self.centery
        self.x2 = self.L * math.cos(alpha2) + self.centerx
        self.y2 = -self.L * math.sin(alpha2) + self.centery
        self.x3 = self.L * math.cos(alpha3) + self.centerx
        self.y3 = -self.L * math.sin(alpha3) + self.centery
        self.x4 = self.L * math.cos(alpha4) + self.centerx
        self.y4 = -self.L * math.sin(alpha4) + self.centery

    def update(self, krachtenlijst):
        '''
        krijgt een lijst binnen van alle werkende krachten op auto en veranderd x,y,v,a,... volgens deze krachten
        :param krachten: krachten lijst , zijnde Fz, Fgas, Frem, Fcoll, (Fvering)
        :return: /
        '''
        total_F = krachten(0, 0, 0, 0)  # is een object krachten() die de som van alle ingegeven/inwerkende krachten op de auto
        for kracht in krachtenlijst:
            total_F += kracht
        total_F.draw(self, color=(0,255,0))
        engine.Label(screen, (50, 50), f"M: {round(total_F.get_M(), 3)}").draw()
        #somF = m*a -> x_a = Fx/m  // y_a = Fy/m
        self.x_a = total_F.get_Fx()/self.mass
        self.x_v += self.x_a
        self.x_v *= 0.999
        self.mapx += self.x_v

        self.y_a = total_F.get_Fy()/self.mass
        self.y_v += self.y_a
        self.y_v *= 0.999
        self.centery += self.y_v

        #somM = I*alpha
        self.alpha = total_F.get_M()/self.I
        self.omega += self.alpha
        self.hoek += self.omega

        self.calculate_pos()

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

#roadsegment class
class Roadsegment:
    def __init__(self,index):
        self.index = index
        self.color = black
        #FUNCTIE VOOR HOOGTE
        self.beginy = WINDOW_SIZE[1]/2 + noise.valueAt(index)*WINDOW_SIZE[1]/3
        self.endy = WINDOW_SIZE[1]/2 + noise.valueAt(index+1)*WINDOW_SIZE[1]/3
        self.width = 5

    def draw(self,mapx):
        self.beginx = WINDOW_SIZE[0]/segments * (self.index - mapx/segments)
        self.endx = WINDOW_SIZE[0]/segments * (self.index + 1 - mapx/segments)
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
    car = Car(WINDOW_SIZE[0]//2, -20, 100, 50, 5)
    g = 0.005
    Fz = krachten(car.mass*g, -math.pi/2, 0, 0)                 #zwaartekracht m*g
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
        if right:
            Fgas = krachten(0.1, car.hoek, -car.L*math.cos(car.hoek+car.hoekpunthoek), car.L*math.sin(car.hoek+car.hoekpunthoek))  # gaskracht waarde kan bepaald worden nu gwn 100
            krachtenlijst.append(Fgas)
        if left:
            Frem = krachten(0.1, math.pi+car.hoek, -car.L*math.cos(car.hoek+car.hoekpunthoek), car.L*math.sin(car.hoek+car.hoekpunthoek))  # remkracht idem
            krachtenlijst.append(Frem)
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

        #auto handelen
        krachtenlijst.append(Fz)

        collisions =[]
        for stuk in road:
            for line in car.collisionbox:
                point = line.collide(stuk)
                if point != None:
                    collisions.append(line.collide(stuk))
        if len(collisions) != 0:
            reactiekracht = reactie(collisions,car)
            krachtenlijst.append(krachten(reactiekracht[0],reactiekracht[1],reactiekracht[2],reactiekracht[3]))

        car.update(krachtenlijst)
        car.draw()

        #krachten tekenen
        for kracht in krachtenlijst:
            kracht.draw(car)


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

#resolutie road
segments = 50


#Noise klaar zetten
noise = Perlin(500//segments) ## frequentie terrain

#road initialiseren
road = []
i = 0
for segment in range(segments):
    road.append(Roadsegment(i))
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
