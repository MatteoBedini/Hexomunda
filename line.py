import pygame
class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), 1)
