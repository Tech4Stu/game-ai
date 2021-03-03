import pygame, sys, os
import engine
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()

#class auto
#heeft pos(y) bep door origin en hoek
#draaien

#munten stacey

#collider

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
    info_label = engine.Label(screen, (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2), "HIER KOMT SPEL", side = "center")
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
WINDOW_SIZE = (window_info.current_w, window_info.current_h) #hoogte/breedte toekennen
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