import sys
import pygame
import random
from pygame.locals import *
from config import *
from init import *
from datetime import datetime

from ObjectSprite import *
from JellyfishSprite import *
from IntroScreen import *

from readfHzaudio import *
from OuttroScreen import *
# ---------------------------------------------
playing = False
running = True
try:
    while running:
        if not playing:
            intro_screen()
            playing = True
            # --------------- init value --------------- #
            img_top = random.choice(objects_top)
            img_button = random.choice(objects_bottom)

            group_jellyfish_man = pygame.sprite.Group()
            group_jellyfish_man.add(
                Jellyfish(
                    jellyfish_img=jellyfish_man_img,
                    jellyfish_num_sub_imgs=3,
                    x_position=int(SCREEN_W * 0.07),
                    y_position=int(SCREEN_H * 0.9)
                )
            )

            group_jellyfish_girl = pygame.sprite.Group()

            count_obj = 0
            OFFSET_NUMBER_OF_OBJ = 2
            is_empty_obj = False
            do_empty_obj = False
            is_win = False
            is_lose = False

            group_object_top = pygame.sprite.Group()
            group_object_top.add(ObjectTop(img_top))

            group_object_bottom = pygame.sprite.Group()
            group_object_bottom.add(ObjectBottom(img_button))

            ADD_object_TOP = pygame.USEREVENT + 1
            pygame.time.set_timer(ADD_object_TOP, 7000)
            ADD_object_BOTTOM = pygame.USEREVENT + 2
            pygame.time.set_timer(ADD_object_BOTTOM, 7000)


        for event in pygame.event.get():
            if event.type == QUIT:  # type: ignore
                running = False
                pygame.quit()
                sys.exit()

            if event.type == ADD_object_TOP and count_obj <= OFFSET_NUMBER_OF_OBJ:
                count_obj += 1
                img_top = random.choice(
                    objects_top) if img_button != object_bottom3 else object_top1
                if len(group_object_top) < 3:
                    group_object_top.add(ObjectTop(img_top))
            if event.type == ADD_object_BOTTOM and count_obj <= OFFSET_NUMBER_OF_OBJ:
                count_obj += 1
                img_button = random.choice(
                    objects_bottom) if img_top != object_top3 else object_bottom1
                if len(group_object_bottom) < 3:
                    group_object_bottom.add(ObjectBottom(img_button))
            if count_obj >= OFFSET_NUMBER_OF_OBJ and len(group_object_top) == 0 and len(group_object_bottom) == 0:
                is_empty_obj = True

        dominant_freq = readfHz()
        screen.fill(BLUESKY)
        screen.blit(bg, bg.get_rect())

        keys = pygame.key.get_pressed()
        # group_jellyfish_man.update()
        group_jellyfish_man.update(keys, dominant_freq)
        group_jellyfish_girl.update(is_auto = True)

        group_object_top.update()
        group_object_bottom.update()

        group_object_top.draw(screen)
        group_object_bottom.draw(screen)
        group_jellyfish_man.draw(screen)
        group_jellyfish_girl.draw(screen)

        hits_top = pygame.sprite.groupcollide(
            group_jellyfish_man, group_object_top, False, False, pygame.sprite.collide_mask
        )
        hits_bottom = pygame.sprite.groupcollide(
            group_jellyfish_man, group_object_bottom, False, False, pygame.sprite.collide_mask
        )
        if len(hits_top) > 0 or len(hits_bottom) > 0:
            if (len(hits_top) > 0):
                first_hit = list(hits_top.values())[0][0]
            elif (len(hits_bottom) > 0):
                first_hit = list(hits_bottom.values())[0][0]
            center = first_hit.rect.center
            is_lose = True
        if is_empty_obj and not do_empty_obj:
            do_empty_obj = True
            group_jellyfish_girl.add(
                Jellyfish(
                    jellyfish_img=jellyfish_girl_cry_img,
                    jellyfish_num_sub_imgs=3,
                    x_position=SCREEN_W + random.randint(0, 500),
                    y_position=int(random.randint(SCREEN_H * 0.2, SCREEN_H * 0.8))
                )
            )

        hits_jellyfish_girl_cry = pygame.sprite.groupcollide(
            group_jellyfish_man, group_jellyfish_girl, True, True, pygame.sprite.collide_mask
        )
        if len(hits_jellyfish_girl_cry) > 0:
            if (len(hits_jellyfish_girl_cry) > 0):
                first_hit = list(hits_jellyfish_girl_cry.values())[0][0]
            center = first_hit.rect.center
            is_win = True
        if is_win:
            outtro_screen(text="You Win", jellyfish_girl_outtro=jellyfish_girl_love_outtro)
            playing = False
        elif (not is_win and do_empty_obj and len(group_jellyfish_girl) == 0) or is_lose:
            outtro_screen(text="You Lose", jellyfish_girl_outtro=jellyfish_girl_cry_outtro)
            playing = False

        pygame.display.flip()
        clock.tick(FPS)
except KeyboardInterrupt:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\nStopped recording.")

except Exception as e:
    # Handle any unexpected errors
    print(f"An error occurred: {e}")

finally:
    # Ensure the stream is closed upon exit
    stream.stop_stream()
    stream.close()
    p.terminate()
