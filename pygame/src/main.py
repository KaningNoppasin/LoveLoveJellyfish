import sys
import pygame
import random
from pygame.locals import *
from config import *
from init import *

from ObjectSprite import *
from JellyfishSprite import *
from IntroScreen import *

import pyaudio
import numpy as np

# Audio configuration
FORMAT = pyaudio.paInt16     # 16-bit resolution
CHANNELS = 1                 # Mono channel
RATE = 44100                 # 44.1kHz sample rate
CHUNK = 1024                 # Number of frames per buffer

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

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
try:
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
                if len(group_object_top) < 3:
                    group_object_top.add(ObjectTop(img_top))
            if event.type == ADD_object_BOTTOM:
                img_button = random.choice(objects_bottom) if img_top != object_top3 else object_bottom1
                if len(group_object_bottom) < 3:
                    group_object_bottom.add(ObjectBottom(img_button))

        data = stream.read(CHUNK, exception_on_overflow=False)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Apply FFT to find frequency spectrum
        fft_data = np.fft.fft(audio_data)

        # Get frequency bins
        freqs = np.fft.fftfreq(len(fft_data), 1 / RATE)

        # Calculate magnitudes and find the dominant frequency
        magnitudes = np.abs(fft_data)
        # Only consider positive frequencies
        dominant_freq = abs(freqs[np.argmax(magnitudes[:CHUNK // 2])])

        # Print the dominant frequency in real-time
        print(f"Real-time Dominant Frequency: {dominant_freq:.2f} Hz")

        screen.fill(BLUESKY)
        screen.blit(bg, bg.get_rect())

        keys = pygame.key.get_pressed()
        group_jellyfish.update(keys, dominant_freq)
        group_object_top.update()
        group_object_bottom.update()

        group_object_top.draw(screen)
        group_object_bottom.draw(screen)
        group_jellyfish.draw(screen)

        hits_top = pygame.sprite.groupcollide(
                group_jellyfish, group_object_top, False, False, pygame.sprite.collide_mask
        )
        hits_bottom = pygame.sprite.groupcollide(
                group_jellyfish, group_object_bottom, False, False, pygame.sprite.collide_mask
        )
        if len(hits_top) > 0 or len(hits_bottom) > 0:
            if(len(hits_top) > 0):
                first_hit = list(hits_top.values())[0][0]
            elif(len(hits_bottom) > 0):
                first_hit = list(hits_bottom.values())[0][0]
            center = first_hit.rect.center
            draw_text('You lose', 36, BLACK,
                screen_rect.centerx, screen_rect.centery)

            # playing = False
        draw_text('Click mouse for game over', 36, BLACK,
                screen_rect.centerx, screen_rect.centery-20)

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