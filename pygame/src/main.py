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
FPS = 30

pygame.init()
pygame.display.set_caption('Introduction to Signals and Systems MiniProject')
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()

#--------------- Images and Sounds ---------------
cover = pygame.transform.scale(pygame.image.load(fr'{imagesPath}cover.jpg'), (SCREEN_W, SCREEN_H))

# ---------------------------------------------
#--------------- Jet Sprite ---------------
jet_img = pygame.image.load(fr'{imagesPath}fighter-jet.png')

class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super(Jet, self).__init__()
        self.image = jet_img
        # self.rect = self.image.get_rect(center=screen_rect.center)
        self.rect = self.image.get_rect(center=(int(SCREEN_W * 0.07),int(SCREEN_H * 0.9)))
        self.distance = 10
        
    def update(self, keys):
        if keys[K_UP]:  # type: ignore
            self.rect.move_ip(0, -self.distance)
            if self.rect.top <= 0:
                self.rect.top = 0

        elif keys[K_DOWN]:  # type: ignore
            self.rect.move_ip(0, self.distance)
            if self.rect.bottom >= SCREEN_H:
                self.rect.bottom = SCREEN_H

#--------------- Cloud Sprite ---------------
# cloud1 = pygame.image.load(fr'{imagesPath}cloud1.png')
# cloud2 = pygame.image.load(fr'{imagesPath}cloud2.png')
# cloud3 = pygame.image.load(fr'{imagesPath}cloud3.png')

cloud1 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj1.png'), (SCREEN_W//3, SCREEN_H//3))
cloud2 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj2.png'), (SCREEN_W//3, SCREEN_H//3))
cloud3 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj3.png'), (SCREEN_W//3, SCREEN_H//3))
cloud4 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj4.png'), (SCREEN_W//3, SCREEN_H//3))
cloud5 = pygame.transform.scale(pygame.image.load(fr'{imagesPath}Obj5.png'), (SCREEN_W//3, SCREEN_H//3))
# clouds = [cloud1, cloud2, cloud3]
clouds = [cloud1, cloud3, cloud4]

class CloudButton(pygame.sprite.Sprite):
    def __init__(self):
        super(CloudButton, self).__init__()
        # self.image = random.choice(clouds)
        self.image = random.choice([cloud5,cloud2])
        # self.image = cloudImage
        h = self.image.get_height()
        start_left = SCREEN_W + random.randint(0, 250)
        # start_left = startLeft
        # start_top =  random.randint(h//2, (SCREEN_H - h))
        start_top =  random.randint(int(SCREEN_H - (h * 1.2)), (SCREEN_H - h))
        # start_top =  SCREEN_H - h
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class CloudTop(pygame.sprite.Sprite):
    def __init__(self):
        super(CloudTop, self).__init__()
        self.image = random.choice(clouds)
        # self.image = cloudImage
        h = self.image.get_height()
        start_left = SCREEN_W + random.randint(250, 500)
        # start_left = startLeft
        # start_top =  random.randint(h//2, (SCREEN_H - h))
        start_top =  random.randint(h//2, (SCREEN_H - h)//2)
        # start_top = 0
        self.rect = self.image.get_rect(topleft=(start_left, start_top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#--------------- Text & Intro Screen ---------------
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
    draw_text('Introduction to Signals and Systems MiniProject', 64, WHITE, cx, 50,fr'{fontsPath}Hyperblox.ttf')

    btn_exit_image = pygame.image.load(fr'{imagesPath}btn-exit.png')
    btn_exit_rect = btn_exit_image.get_rect(right=cx-30, top=int(SCREEN_H * 0.75))

    btn_start_image = pygame.image.load(fr'{imagesPath}btn-start.png')
    btn_start_rect = btn_start_image.get_rect(left=cx+30, top=int(SCREEN_H * 0.75))

    screen.blit(btn_start_image, btn_start_rect)
    screen.blit(btn_exit_image, btn_exit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN: # type: ignore
                if btn_start_rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False
                elif btn_exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()



group_jet = pygame.sprite.Group()
group_jet.add(Jet())

group_cloud_top = pygame.sprite.Group()
group_cloud_top.add(CloudTop())

group_cloud_button = pygame.sprite.Group()
group_cloud_button.add(CloudButton())

ADD_CLOUD_TOP = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_CLOUD_TOP, 2500)
ADD_CLOUD_BUTTON = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD_BUTTON, 1500)
# ---------------------------------------------
playing = False
running = True
while running:
    if not playing:
        intro_screen()
        playing = True

    for event in pygame.event.get():
        if event.type == QUIT: # type: ignore
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN: # type: ignore
            playing = False
        elif event.type == ADD_CLOUD_TOP:
            group_cloud_top.add(CloudTop())
            # group_cloud_button.add(CloudButton())
        elif event.type == ADD_CLOUD_BUTTON:
            # group_cloud_top.add(CloudTop())
            group_cloud_button.add(CloudButton())

    screen.fill(BLUESKY)

    keys = pygame.key.get_pressed()
    group_jet.update(keys)
    group_cloud_top.update()
    group_cloud_button.update()

    group_jet.draw(screen)
    group_cloud_top.draw(screen)
    group_cloud_button.draw(screen)
    draw_text('Click mouse for game over', 36, WHITE,screen_rect.centerx, screen_rect.centery-20)

    pygame.display.flip()
