import pygame
from pygame.locals import *
from config import *
import random
from init import *

# --------------- Jellyfish Sprite ---------------
jellyfish_man_img = pygame.transform.scale(pygame.image.load(fr'{imagesPath}JellyfishM.png'), (SCREEN_W//3.5, SCREEN_H//3.5))
jellyfish_girl_love_img = pygame.transform.scale(pygame.image.load(fr'{imagesPath}JellyfishGL.png'), (SCREEN_W//3.5, SCREEN_H//3.5))
jellyfish_girl_cry_img = pygame.transform.scale(pygame.image.load(fr'{imagesPath}JellyfishGC.png'), (SCREEN_W//3.5, SCREEN_H//3.5))

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, jellyfish_img, jellyfish_num_sub_imgs, x_position, y_position):
        super(Jellyfish, self).__init__()

        # jellyfish_num_sub_imgs = 3
        jellyfish_sub_img_w = jellyfish_img.get_width() // jellyfish_num_sub_imgs
        jellyfish_sub_img_h = jellyfish_img.get_height()
        self.jellyfish_sub_imgs = []

        for i in range(jellyfish_num_sub_imgs):
            x = i * jellyfish_sub_img_w
            f = jellyfish_img.subsurface(x, 0, jellyfish_sub_img_w, jellyfish_sub_img_h)
            self.jellyfish_sub_imgs.append(f)

        self.jellyfish_repeat = FPS // jellyfish_num_sub_imgs
        self.jellyfish_last_frame = (jellyfish_num_sub_imgs * self.jellyfish_repeat) - 1

        self.image = self.jellyfish_sub_imgs[0]
        # self.rect = self.image.get_rect(center=(int(SCREEN_W * 0.07), int(SCREEN_H * 0.9)))
        self.rect = self.image.get_rect(center=(x_position, y_position))
        self.index = 0
        self.speedx = 5
        self.distance = 10

    def update_animation(self):
        if self.index >= self.jellyfish_last_frame:
            self.index = 0

        i = self.index // self.jellyfish_repeat
        self.image = self.jellyfish_sub_imgs[i]
        self.index += 1

    def update_movement(self, keys = None, dominant_freq = None):
        if keys is None and dominant_freq is None: return

        if keys[K_UP] or dominant_freq > 800:  # type: ignore
            self.rect.move_ip(0, -self.distance)
            if self.rect.top <= 0:
                self.rect.top = 0
        else:
            self.rect.move_ip(0, self.distance)
            if self.rect.bottom >= SCREEN_H:
                self.rect.bottom = SCREEN_H

    def update(self, keys = None, dominant_freq = None):
        self.update_animation()
        self.update_movement(keys, dominant_freq)