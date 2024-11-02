import pygame
from config import *
import random
from init import *

# --------------- Object Sprite ---------------
object1 = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}Obj1.png'), (SCREEN_W//2.5, SCREEN_H//2.5))
object2 = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}Obj2.png'), (SCREEN_W//2.5, SCREEN_H//2.5))
object3 = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}Obj3.png'), (SCREEN_W//2.5, SCREEN_H//2.5))
object4 = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}Obj4.png'), (SCREEN_W//2.5, SCREEN_H//2.5))
# object5 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj5.png'), (SCREEN_W//2.5, SCREEN_H//2.5))
object5 = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}draft.png'), (SCREEN_H//2.5, SCREEN_W//2.5))
# object5 = pygame.image.load(fr'{imagesPath}draft.png')
# objects = [object1, object2, object3]
objects = [object1, object3, object4]


class ObjectButton(pygame.sprite.Sprite):
    def __init__(self):
        super(ObjectButton, self).__init__()
        # self.image = random.choice(objects)
        self.image = random.choice([object5, object2])
        # self.image = objectImage
        h = self.image.get_height()
        # start_left = SCREEN_W + random.randint(0, 500)
        start_left = SCREEN_W + 1200
        # start_left = startLeft
        # start_top =  random.randint(h//2, (SCREEN_H - h))
        # start_top =  random.randint(int(SCREEN_H - (h * 1.2)), (SCREEN_H - h))
        start_top = SCREEN_H - h
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class ObjectTop(pygame.sprite.Sprite):
    def __init__(self):
        super(ObjectTop, self).__init__()
        self.image = random.choice(objects)
        # self.image = objectImage
        h = self.image.get_height()
        # start_left = SCREEN_W + random.randint(0, 500)
        start_left = SCREEN_W + 500
        # start_left = startLeft
        # start_top =  random.randint(h//2, (SCREEN_H - h))
        # start_top =  random.randint(h//2, (SCREEN_H - h)//2)
        start_top = 0
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
