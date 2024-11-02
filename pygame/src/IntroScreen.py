import sys
import pygame
from pygame.locals import *
from config import *
from init import *

# --------------- Text & Intro Screen ---------------


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
    draw_text('Introduction to Signals and Systems MiniProject',
              64, WHITE, cx, 50, fr'{fontsPath}Hyperblox.ttf')

    btn_exit_image = pygame.image.load(fr'{imagesPath}btn-exit.png')
    btn_exit_rect = btn_exit_image.get_rect(
        right=cx-30, top=int(SCREEN_H * 0.75))

    btn_start_image = pygame.image.load(fr'{imagesPath}btn-start.png')
    btn_start_rect = btn_start_image.get_rect(
        left=cx+30, top=int(SCREEN_H * 0.75))

    screen.blit(btn_start_image, btn_start_rect)
    screen.blit(btn_exit_image, btn_exit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:  # type: ignore
                if btn_start_rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False
                elif btn_exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()