#esempio per gif animata

import pygame
import sys
from PIL import Image, ImageSequence

pygame.init()
clock = pygame.time.Clock()

# Imposta le dimensioni della finestra
screen = pygame.display.set_mode((400, 400))

# Carica l'immagine GIF animata
gif = Image.open("animated.gif")

# Estrai tutte le immagini dal GIF

frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in ImageSequence.Iterator(gif)]

frame_rate = 5 # Regola il frame rate come desideri
current_frame = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pulisci la schermata
    screen.fill((255, 255, 255))

    # Visualizza il frame corrente
    screen.blit(frames[current_frame], (0, 0))

    current_frame = (current_frame + 1) % len(frames)  # Loop tra i frame

    pygame.display.flip()
    clock.tick(frame_rate)

pygame.quit()
sys.exit()





#options menu button
            