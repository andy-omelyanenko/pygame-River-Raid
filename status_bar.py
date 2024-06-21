import _globals
import sprites
import pygame

pygame.font.init()
_font = pygame.font.SysFont('Comic Sans MS', 28)


def fill_with_black():
    # Drawing Rectangle
    pygame.draw.rect(_globals.Screen, (0, 0, 0), pygame.Rect(0, _globals.GAME_SCREEN_HEIGHT, _globals.SCREEN_WIDTH, _globals.SCREEN_HEIGHT))


def display_lives():
    text_surface = _font.render('Lives: ' + str(sprites.Player.Lives), False, (255, 255, 255))
    _globals.Screen.blit(text_surface, (10, _globals.GAME_SCREEN_HEIGHT))


def display_score():
    text_surface = _font.render('Score: ' + str(sprites.Player.Score), False, (255, 255, 255))
    _globals.Screen.blit(text_surface, (150, _globals.GAME_SCREEN_HEIGHT))


def display_fuel():
    text_surface = _font.render('Fuel: ' + str(int(sprites.Player.Fuel)), False, (255, 255, 255))
    _globals.Screen.blit(text_surface, (370, _globals.GAME_SCREEN_HEIGHT))


def display_area():
    text_surface = _font.render('Bridge: ' + str(_globals.Area + 1), False, (255, 255, 255))
    _globals.Screen.blit(text_surface, (525, _globals.GAME_SCREEN_HEIGHT))
