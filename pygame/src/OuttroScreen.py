import sys
import pygame
from pygame.locals import *
from config import *
from init import *
from JellyfishSprite import *
# --------------- Text & Intro Screen ---------------
jellyfish_man_outtro = Jellyfish(
    jellyfish_img=jellyfish_man_img,
    jellyfish_num_sub_imgs=3,
    x_position=int(SCREEN_W // 2 - SCREEN_W * 0.05),
    y_position=int(SCREEN_H // 2)
)
jellyfish_girl_love_outtro = Jellyfish(
    jellyfish_img=jellyfish_girl_love_img,
    jellyfish_num_sub_imgs=3,
    x_position=int(SCREEN_W // 2 + SCREEN_W * 0.05),
    y_position=int(SCREEN_H // 2)
)
jellyfish_girl_cry_outtro = Jellyfish(
    jellyfish_img=jellyfish_girl_cry_img,
    jellyfish_num_sub_imgs=3,
    x_position=int(SCREEN_W // 2 + SCREEN_W * 0.05),
    y_position=int(SCREEN_H // 2)
)

def draw_text(text, size, color, x, y, fontFile=None):
    if fontFile == None:
        font = pygame.font.SysFont(None, size)
    else:
        font = pygame.font.Font(fontFile, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)


def outtro_screen(text, jellyfish_girl_outtro):

    waiting = True
    while waiting:
        screen.fill(BLUE)
        screen.blit(bg, bg.get_rect())
        cx = screen_rect.centerx

        btn_exit_image = pygame.transform.scale(pygame.image.load(fr'{imagesPath}btn-exit.png'),(SCREEN_W // 15, SCREEN_H // 15))
        btn_exit_rect = btn_exit_image.get_rect(
            right=cx-30, top=int(SCREEN_H * 0.85))

        btn_start_image = pygame.transform.scale(pygame.image.load(fr'{imagesPath}btn-start.png'),(SCREEN_W // 15, SCREEN_H // 15))
        btn_start_rect = btn_start_image.get_rect(
            left=cx+30, top=int(SCREEN_H * 0.85))
        draw_text(text, 64, BLACK,
                      screen_rect.centerx, screen_rect.centery - 200, fr'{fontsPath}SmothyBubble.com.otf')

        jellyfish_man_outtro.update()
        jellyfish_girl_outtro.update()

        screen.blit(jellyfish_man_outtro.image, jellyfish_man_outtro.rect)
        screen.blit(jellyfish_girl_outtro.image,
                    jellyfish_girl_outtro.rect)

        screen.blit(btn_start_image, btn_start_rect)
        screen.blit(btn_exit_image, btn_exit_rect)

        pygame.display.flip()
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