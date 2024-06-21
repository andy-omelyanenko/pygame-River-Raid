from pygame import *
import _globals
from sprites import Player
from sounds import *

pygame.font.init()
_font = pygame.font.SysFont('Comic Sans MS', 16)
_font_big = pygame.font.SysFont('Comic Sans MS', 42)
_font_small = pygame.font.SysFont('Consolas', 12)


def Congratulations():
    Sounds.landed()
    pygame.time.wait(4100)

    img = pygame.image.load("rsc/images/Congratulations.png").convert_alpha()
    rect = img.get_rect()
    rect.center = (230, 110)
    _globals.Screen.blit(img, rect)

    img = pygame.image.load("rsc/images/medal1.png").convert_alpha()
    rect = img.get_rect()
    rect.center = (150, 145)
    _globals.Screen.blit(img, rect)
    pygame.display.update()
    Sounds.medal()
    pygame.time.wait(300)

    img = pygame.image.load("rsc/images/medal2.png").convert_alpha()
    rect = img.get_rect()
    rect.center = (173, 145)
    _globals.Screen.blit(img, rect)
    pygame.display.update()
    Sounds.medal()
    pygame.time.wait(300)

    img = pygame.image.load("rsc/images/medal3.png").convert_alpha()
    rect = img.get_rect()
    rect.center = (320, 132)
    _globals.Screen.blit(img, rect)
    pygame.display.update()
    Sounds.medal()
    pygame.time.wait(3000)

    Sounds.anthem(True)

    wait_for_key_press()


def Intro():
    _globals.Screen.fill((0, 0, 0))
    img = pygame.image.load("rsc/images/intro.png").convert_alpha()
    rect = img.get_rect()
    rect.left = 0
    rect.top = 0
    _globals.Screen.blit(img, rect)

    text_surface = _font_big.render('River Raid', False, (30, 90, 255))
    _globals.Screen.blit(text_surface, (20, 20))

    text_surface = _font.render('Controls:', False, (255, 255, 224))
    _globals.Screen.blit(text_surface, (492, 0))

    text_surface = _font.render('Cursor Keys to move', False, (255, 255, 224))
    _globals.Screen.blit(text_surface, (492, 30))

    text_surface = _font.render('SPACE to fire', False, (255, 255, 224))
    _globals.Screen.blit(text_surface, (490, 57))

    text_surface = _font.render('P or Pause to pause', False, (255, 255, 224))
    _globals.Screen.blit(text_surface, (492, 85))

    text_surface = _font.render('ESC to quit', False, (255, 255, 224))
    _globals.Screen.blit(text_surface, (492, 170))

    text_surface = _font.render('Press SPACE to start', False, (250, 250, 50))
    _globals.Screen.blit(text_surface, (492, 353))

    text_surface = _font_small.render('Pygame by Andy Omelyanenko in 2024', False, (111, 111, 111))
    _globals.Screen.blit(text_surface, (9, 363))

    pygame.display.update()
    Sounds.music(True)


def wait_for_key_press():
    is_key_pressed = False
    while not is_key_pressed and not Player.is_ESC_pressed:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Player.is_flying = False
                    Player.Game_Over = True
                    Player.is_ESC_pressed = True
            else:
                if (event.type == KEYUP) and (event.key != K_ESCAPE):
                    return True
