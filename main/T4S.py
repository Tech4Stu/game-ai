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
#foto's
logo_img = pygame.image.load("T4S_logo.png").convert()
logo_img.set_colorkey((255,255,255))
#knoppen
#play_button = engine.Button(screen, (50, WINDOW_SIZE[1]-250), "PLAY", font_size=120)
#upgrade_button = engine.Button(screen, (100+play_button.width, WINDOW_SIZE[1]-250), "UPGRADES", font_size=120)
#settings_button = engine.Button(screen, (150+play_button.width+upgrade_button.width, WINDOW_SIZE[1]-250), "SETTINGS", font_size=120)

play_button = engine.Button(screen, (50, WINDOW_SIZE[1]-250), "PLAY", font_size=120, transparant=True)
upgrade_button = engine.Button(screen, (play_button.pos[0]+play_button.width+50, WINDOW_SIZE[1]-250), "UPGRADES", font_size=120, transparant=True)
settings_button = engine.Button(screen, (upgrade_button.pos[0]+upgrade_button.width+50, WINDOW_SIZE[1]-250), "SETTINGS", font_size=120, transparant=True)
titel_label = engine.Label(screen, (200, 150), "NAAM", font_size=240, transparant=True)
AI_label = engine.Label(screen, (800, 350), "(AI)", font_size=140, transparant=True)

run = True
while run:
    screen.fill((100,100,150))
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
    titel_label.draw()
    AI_label.draw()
    screen.blit(pygame.transform.scale(logo_img, (100,100)), (WINDOW_SIZE[0]-110, WINDOW_SIZE[1]-110-30))

    clock.tick(60)
    pygame.display.update()