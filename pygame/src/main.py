import sys
import pygame
import random
from pygame.locals import *
from config import *

SCREEN_W = 1920
SCREEN_H = 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUESKY = (200, 220, 255)
BLUE = (0, 0, 255)
FPS = 60

pygame.init()
pygame.display.set_caption('Introduction to Signals and Systems MiniProject')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()

# --------------- Images and Sounds ---------------
cover = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}cover.jpg'), (SCREEN_W, SCREEN_H))
bg = pygame.transform.scale(pygame.image.load(
    fr'{imagesPath}bg.png'), (SCREEN_W, SCREEN_H))

# ---------------------------------------------

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


# --------------- jellyfish Sprite ---------------
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

    def update(self, keys):
        if self.index >= jellyfish_last_frame:
            self.index = 0

        i = self.index // jellyfish_repeat
        self.image = jellyfish_sub_imgs[i]
        self.index += 1

        if keys[K_UP]:  # type: ignore
            self.rect.move_ip(0, -self.distance)
            if self.rect.top <= 0:
                self.rect.top = 0

        elif keys[K_DOWN]:  # type: ignore
            self.rect.move_ip(0, self.distance)
            if self.rect.bottom >= SCREEN_H:
                self.rect.bottom = SCREEN_H

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
