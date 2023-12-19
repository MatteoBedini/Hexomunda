#prova per animazioni

import pygame

pygame.init()

pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(144)
    fpss = clock.get_fps()

    # Print FPS to console
    print(f"FPS: {fpss}")
    pygame.display.flip()

pygame.quit()