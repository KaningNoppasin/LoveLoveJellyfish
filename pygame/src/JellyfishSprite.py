import pygame
from pygame.locals import *
from config import *
import random
from init import *

# --------------- Jellyfish Sprite ---------------
jellyfish_img = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}Jellyfish.png'), (SCREEN_W//3.5, SCREEN_H//3.5))
jellyfish_num_sub_imgs = 3
jellyfish_sub_img_w = jellyfish_img.get_width() // jellyfish_num_sub_imgs
jellyfish_sub_img_h = jellyfish_img.get_height()
jellyfish_sub_imgs = []

for i in range(jellyfish_num_sub_imgs):
    x = i * jellyfish_sub_img_w
    f = jellyfish_img.subsurface(x, 0, jellyfish_sub_img_w, jellyfish_sub_img_h)
    jellyfish_sub_imgs.append(f)

jellyfish_repeat = FPS // jellyfish_num_sub_imgs
jellyfish_last_frame = (jellyfish_num_sub_imgs * jellyfish_repeat) - 1


class Jellyfish(pygame.sprite.Sprite):
    def __init__(self):
        super(Jellyfish, self).__init__()
        self.image = jellyfish_sub_imgs[0]
        self.rect = self.image.get_rect(
            center=(int(SCREEN_W * 0.07), int(SCREEN_H * 0.9)))
        self.index = 0
        self.speedx = 5
        self.distance = 10

    def update(self, keys, dominant_freq):
        if self.index >= jellyfish_last_frame:
            self.index = 0

        i = self.index // jellyfish_repeat
        self.image = jellyfish_sub_imgs[i]
        self.index += 1

        if keys[K_UP] or dominant_freq > 800:  # type: ignore
            self.rect.move_ip(0, -self.distance)
            if self.rect.top <= 0:
                self.rect.top = 0

        elif keys[K_DOWN]:  # type: ignore
            self.rect.move_ip(0, self.distance)
            if self.rect.bottom >= SCREEN_H:
                self.rect.bottom = SCREEN_H
        else:
            self.rect.move_ip(0, self.distance)
            if self.rect.bottom >= SCREEN_H:
                self.rect.bottom = SCREEN_H