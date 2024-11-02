import sys
import pygame
import random
from pygame.locals import *
from config import *
from init import *

from ObjectSprite import *
from JellyfishSprite import *
from IntroScreen import *

img_top = random.choice(objects_top)
img_button = random.choice(objects_bottom)

group_jellyfish = pygame.sprite.Group()
group_jellyfish.add(Jellyfish())


group_object_top = pygame.sprite.Group()
group_object_top.add(ObjectTop(img_top))

group_object_bottom = pygame.sprite.Group()
group_object_bottom.add(ObjectBottom(img_button))

ADD_object_TOP = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_object_TOP, 7000)
ADD_object_BOTTOM = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_object_BOTTOM, 7000)
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

        if event.type == ADD_object_TOP:
            img_top = random.choice(objects_top) if img_button != object_bottom3 else object_top1
            if len(group_object_top) < 5:
                group_object_top.add(ObjectTop(img_top))
        if event.type == ADD_object_BOTTOM:
            img_button = random.choice(objects_bottom) if img_top != object_top3 else object_bottom1
            if len(group_object_bottom) < 5:
                group_object_bottom.add(ObjectBottom(img_button))

    screen.fill(BLUESKY)
    screen.blit(bg, bg.get_rect())

    keys = pygame.key.get_pressed()
    group_jellyfish.update(keys)
    group_object_top.update()
    group_object_bottom.update()

    group_object_top.draw(screen)
    group_object_bottom.draw(screen)
    group_jellyfish.draw(screen)
    draw_text('Click mouse for game over', 36, BLACK,
              screen_rect.centerx, screen_rect.centery-20)

    pygame.display.flip()
