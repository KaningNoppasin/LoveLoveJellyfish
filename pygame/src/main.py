# ตัวอย่าง 13-5

import sys
import pygame
import random
from pygame.locals import *

SCREEN_W = 1920
SCREEN_H = 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
FPS = 30

pygame.init()
pygame.display.set_caption('Pygame')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()
img_path = r'./asset/images/fortest'

# ---------------------------------------------


def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)


def intro_screen():
    screen.fill(BLUE)
    cx = screen_rect.centerx
    draw_text('Pygame', 64, cx, 50)

    btn_exit_image = pygame.image.load(fr'{img_path}/btn-exit.png')
    btn_exit_rect = btn_exit_image.get_rect(right=cx-30, top=int(SCREEN_H * 0.75))

    btn_start_image = pygame.image.load(fr'{img_path}/btn-start.png')
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
    draw_text('Click mouse for game over', 36,
              screen_rect.centerx, screen_rect.centery-20)

    pygame.display.flip()
