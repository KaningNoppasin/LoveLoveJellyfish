import sys
import pygame
from pygame.locals import *
from config import *
from init import *
from JellyfishSprite import *
# --------------- Text & Intro Screen ---------------
jellyfish_man_intro = Jellyfish(
    jellyfish_img=jellyfish_man_img,
    jellyfish_num_sub_imgs=3,
    x_position=int(SCREEN_W // 2 - SCREEN_W * 0.3),
    y_position=int(SCREEN_H // 2)
)
jellyfish_girl_cry_intro = Jellyfish(
    jellyfish_img=jellyfish_girl_cry_img,
    jellyfish_num_sub_imgs=3,
    x_position=int(SCREEN_W // 2 + SCREEN_W * 0.3),
    y_position=int(SCREEN_H // 2)
)


game_description = {
    'game_description': [
        "Game Description:",
        "In Love Love Jellyfish, players step into the translucent world",
        "of a determined jellyfish on a mission to find and rescue",
        "his beloved. The jellyfish’s girlfriend is trapped in the",
        "deep sea, and our hero must navigate through an underwater",
        "maze of obstacles to reach her. The ocean is filled with",
        "floating debris, dangerous sea creatures, and mysterious",
        "objects that, if hit, will cause him to lose his energy",
        "and restart his journey."
    ],
    'gameplay_mechanics': [
        "Gameplay Mechanics:",
        "Frequency Control: Players use their own voice or",
        "a frequency controller to adjust the jellyfish’s movement",
        "and frequency, avoiding obstacles. Humming or adjusting",
        "pitch lets the jellyfish dodge, dive, or rise as needed."
    ]
}

# Define ratios for font sizes and margins
TITLE_FONT_SIZE_RATIO = 128 / 1080  # Original title size was 128
HEADER_FONT_SIZE_RATIO = 50 / 1080  # Original header size was 50
TEXT_FONT_SIZE_RATIO = 42 / 1080     # Original text size was 42
MARGIN_RATIO = 5 / 1080              # Original margin was 40


def draw_text(text, size, color, x, y, fontFile=None):
    if fontFile == None:
        font = pygame.font.SysFont(None, size)
    else:
        font = pygame.font.Font(fontFile, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)


def render_text_responsive(screen_width, screen_height, text_data):
    cx = screen_rect.centerx

    # Calculate responsive title font size
    title_font_size = int(screen_height * TITLE_FONT_SIZE_RATIO)

    # Calculate y position for title
    # Position for title at the top
    title_y_position = int(screen_height * 0.05)

    # Render the title
    draw_text('Love Love Jellyfish', title_font_size, DARK_ORCHID,
              cx, title_y_position, fr'{fontsPath}SmothyBubble.com.otf')

    # Calculate responsive sizes
    header_font_size = int(screen_height * HEADER_FONT_SIZE_RATIO)
    text_font_size = int(screen_height * TEXT_FONT_SIZE_RATIO)
    margin = int(screen_height * MARGIN_RATIO)

    # Calculate initial y position for game description
    # y_position = int(screen_height * 0.23)  # 250px as a ratio of 1080
    y_position = int(screen_height * 0.2)  # 250px as a ratio of 1080

    # Render game description
    for line in text_data['game_description']:
        draw_text(line, text_font_size if line != "Game Description:" else header_font_size,
                  DARK_ORCHID, cx, y_position, fr'{fontsPath}Quethy.ttf')
        y_position += text_font_size + margin

    # Add some space before the next section
    y_position += margin * 2

    # Render gameplay mechanics
    for line in text_data['gameplay_mechanics']:
        draw_text(line, text_font_size if line != "Gameplay Mechanics:" else header_font_size,
                  DARK_ORCHID, cx, y_position, fr'{fontsPath}Quethy.ttf')
        y_position += text_font_size + margin


def intro_screen():

    waiting = True
    while waiting:
        screen.fill(BLUE)
        screen.blit(bg, bg.get_rect())
        cx = screen_rect.centerx

        render_text_responsive(SCREEN_W, SCREEN_H, game_description)

        btn_exit_image = pygame.image.load(fr'{imagesPath}btn-exit.png')
        btn_exit_rect = btn_exit_image.get_rect(
            right=cx-30, top=int(SCREEN_H * 0.85))

        btn_start_image = pygame.image.load(fr'{imagesPath}btn-start.png')
        btn_start_rect = btn_start_image.get_rect(
            left=cx+30, top=int(SCREEN_H * 0.85))

        jellyfish_man_intro.update()
        jellyfish_girl_cry_intro.update()

        screen.blit(jellyfish_man_intro.image, jellyfish_man_intro.rect)
        screen.blit(jellyfish_girl_cry_intro.image,
                    jellyfish_girl_cry_intro.rect)

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
