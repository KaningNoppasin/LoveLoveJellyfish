import pygame
from config import *
import random
from init import *

# --------------- Object Sprite ---------------
object_bottom1 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectBottom1.png'), (SCREEN_H//2.5, SCREEN_W//2.5))
object_bottom2 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectBottom2.png'), (SCREEN_H//2.5, SCREEN_W//2.5))
object_bottom3 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectBottom3.png'), (SCREEN_H//2.5, SCREEN_W//2.5))

object_top1 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectTop1.png'), (SCREEN_H//2.5, SCREEN_W//2.5))
object_top2 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectTop2.png'), (SCREEN_H//2.5, SCREEN_W//2.5))
object_top3 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Object/ObjectTop3.png'), (SCREEN_H//2.5, SCREEN_W//2.5))

objects_bottom = [object_bottom1, object_bottom2, object_bottom3]
objects_top = [object_top1, object_top2, object_top3]


class ObjectBottom(pygame.sprite.Sprite):
    def __init__(self, image = None):
        super(ObjectBottom, self).__init__()
        self.image = random.choice(objects_bottom) if image == None else image
        # self.image = objectImage
        h = self.image.get_height()
        # start_left = SCREEN_W + random.randint(0, 500)
        start_left = SCREEN_W + random.choice([random.randint(0, 200), random.randint(700, 900)])
        # start_left = SCREEN_W + 700
        start_top = SCREEN_H - h
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class ObjectTop(pygame.sprite.Sprite):
    def __init__(self, image = None):
        super(ObjectTop, self).__init__()
        self.image = random.choice(objects_top) if image == None else image
        h = self.image.get_height()
        # start_left = SCREEN_W + random.randint(0, 500)
        start_left = SCREEN_W + random.randint(400, 500)
        # start_left = SCREEN_W + 100
        start_top = 0
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
