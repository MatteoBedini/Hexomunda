import pygame

# Inizializzazione di Pygame
pygame.init()

# Impostazione delle dimensioni della finestra
larghezza = 400
altezza = 300
finestra = pygame.display.set_mode((larghezza, altezza))
pygame.display.set_caption('Rettangolo con lati colorati')

# Posizione e dimensioni del rettangolo
x = 50
y = 50
larghezza_rettangolo = 200
altezza_rettangolo = 100

# Colori dei lati
rosso = (255, 0, 0)
verde = (0, 255, 0)
blu = (0, 0, 255)
giallo = (255, 255, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    finestra.fill((255, 255, 255))  # Sfondo bianco

    # Disegno dei lati del rettangolo con colori diversi
    pygame.draw.line(finestra, blu, (x, y), (x, y + altezza_rettangolo), 3)  # Lato sinistro (blu)
    pygame.draw.line(finestra, verde, (x + larghezza_rettangolo, y), (x + larghezza_rettangolo, y + altezza_rettangolo), 3)  # Lato destro (verde)
    pygame.draw.line(finestra, giallo, (x, y), (x + larghezza_rettangolo, y), 3)  # Lato superiore (giallo)
    pygame.draw.line(finestra, rosso, (x, y + altezza_rettangolo), (x + larghezza_rettangolo, y + altezza_rettangolo), 3)  # Lato inferiore (rosso)

    pygame.display.update()

pygame.quit()