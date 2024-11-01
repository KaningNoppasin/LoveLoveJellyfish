# ตัวอย่าง 13-5

import sys
import pygame
import random
from pygame.locals import *
from config import *

SCREEN_W = 1920
SCREEN_H = 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
FPS = 30

pygame.init()
pygame.display.set_caption('Introduction to Signals and Systems MiniProject')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()


cover = pygame.transform.scale(pygame.image.load(fr'{imagesPath}cover.jpg'), (SCREEN_W, SCREEN_H))

# ---------------------------------------------


#--------------- Text & Intro Screen ---------------
def draw_text(text, size, color, x, y, fontFile=None):
    if fontFile == None:
        font = pygame.font.SysFont(None, size)
    else:
        font = pygame.font.Font(fontFile, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)


def intro_screen():
    screen.fill(BLUE)

    screen.blit(cover, cover.get_rect())
    cx = screen_rect.centerx
    draw_text('Introduction to Signals and Systems MiniProject', 64, WHITE, cx, 50,fr'{fontsPath}Hyperblox.ttf')

    btn_exit_image = pygame.image.load(fr'{imagesPath}btn-exit.png')
    btn_exit_rect = btn_exit_image.get_rect(right=cx-30, top=int(SCREEN_H * 0.75))

    btn_start_image = pygame.image.load(fr'{imagesPath}btn-start.png')
    btn_start_rect = btn_start_image.get_rect(left=cx+30, top=int(SCREEN_H * 0.75))

    screen.blit(btn_start_image, btn_start_rect)
    screen.blit(btn_exit_image, btn_exit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN: # type: ignore
                if btn_start_rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False
                elif btn_exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()


# ---------------------------------------------
playing = False
running = True
while running:
    if not playing:
        intro_screen()
        playing = True

    for e in pygame.event.get():
        if e.type == QUIT: # type: ignore
            running = False
            pygame.quit()
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN: # type: ignore
            playing = False

    screen.fill(BLACK)
    draw_text('Click mouse for game over', 36, WHITE,screen_rect.centerx, screen_rect.centery-20)

    pygame.display.flip()
