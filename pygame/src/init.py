import pygame
from config import *

SCREEN_W = 1280
SCREEN_H = 720
# SCREEN_W = 1920
# SCREEN_H = 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUESKY = (200, 220, 255)
BLUE = (0, 0, 255)
# DARK_ORCHID = 		(252,130,191)
PINK = (252,130,191)
DEEP_SKY_BLUE = (0,191,255)
VIOLET = (30,144,255)
FPS = 60

# --------------- Images and Sounds ---------------
bg = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Background.jpg'), (SCREEN_W, SCREEN_H))
bg_blur = pygame.transform.scale(pygame.image.load(fr'{imagesPath}BGblurr.jpg'), (SCREEN_W, SCREEN_H))

# ---------------------------------------------

pygame.init()
pygame.display.set_caption('Introduction to Signals and Systems MiniProject')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()

# ---------------------------------------------