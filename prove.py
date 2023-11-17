#prova per animazioni

import pygame
import sys
import os

# Inizializza Pygame
pygame.init()

# Imposta il display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Idle Animation")

# Carica le immagini
image_folder = "path/to/your/image/folder"
idle_images = [pygame.image.load(os.path.join(image_folder, f"idle_{i}.png")) for i in range(1, 11)]  # Supponendo 10 frame

# Imposta le variabili
clock = pygame.time.Clock()
animation_speed = 0.2  # Regola questa variabile per cambiare la velocità dell'animazione
current_frame = 0
elapsed_time = 0

# Ciclo principale del gioco
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calcola il tempo trascorso
    elapsed_time += clock.get_rawtime()
    clock.tick_busy_loop(60)  # Imposta una frequenza di clock

    # Aggiorna l'animazione in base al tempo trascorso
    if elapsed_time >= animation_speed * 1000:  # Converti la velocità in millisecondi
        current_frame = (current_frame + 1) % len(idle_images)
        elapsed_time = 0

    # Disegna il frame corrente
    screen.fill((255, 255, 255))  # Riempie lo sfondo di bianco
    screen.blit(idle_images[current_frame], (width // 2 - idle_images[current_frame].get_width() // 2, height // 2 - idle_images[current_frame].get_height() // 2))

    # Aggiorna il display
    pygame.display.flip()