import sys
import pygame
import random
from pygame.locals import *
from config import *
from init import *

from ObjectSprite import *
from JellyfishSprite import *
from IntroScreen import *

group_jellyfish = pygame.sprite.Group()
group_jellyfish.add(Jellyfish())


group_object_top = pygame.sprite.Group()
group_object_top.add(ObjectTop())

group_object_button = pygame.sprite.Group()
group_object_button.add(ObjectButton())

ADD_object_TOP = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_object_TOP, 7000)
ADD_object_BUTTON = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_object_BUTTON, 7000)
# ---------------------------------------------
playing = False
running = True
while running:
    if not playing:
        intro_screen()
        playing = True

    for event in pygame.event.get():
        if event.type == QUIT:  # type: ignore
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:  # type: ignore
            playing = False
        elif event.type == ADD_object_TOP:
            if len(group_object_top) < 5:
                group_object_top.add(ObjectTop())
        elif event.type == ADD_object_BUTTON:
            if len(group_object_button) < 5:
                group_object_button.add(ObjectButton())

    screen.fill(BLUESKY)
    screen.blit(bg, bg.get_rect())

    keys = pygame.key.get_pressed()
    group_jellyfish.update(keys)
    group_object_top.update()
    group_object_button.update()

    group_object_top.draw(screen)
    group_object_button.draw(screen)
    group_jellyfish.draw(screen)
    draw_text('Click mouse for game over', 36, BLACK,
              screen_rect.centerx, screen_rect.centery-20)

    pygame.display.flip()
