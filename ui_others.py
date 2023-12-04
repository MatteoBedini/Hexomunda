import pygame
import Main

class Scrollbar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroller=Scroller(x,y,width,height/10,self)
        self.rect=pygame.Rect(x,y,width,height)
        self.color=(0,0,0,0)

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.scroller.draw(screen)




class Scroller:
    def __init__(self, x, y, width, height, parentbar):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect=pygame.Rect(x,y,width,height)
        self.dragging=False
        self.parentbar=parentbar
        self.color=(0,0,0,0)
        self.startingy=y

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def input(self):

        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False

            if self.dragging and event.type == pygame.MOUSEMOTION:
                if event.pos[1]<self.parentbar.y+self.height:
                    self.rect.y = self.parentbar.y
                elif event.pos[1]>self.parentbar.y+self.parentbar.height-self.height:
                    self.rect.y = self.parentbar.y+self.parentbar.height-self.height
                else:
                    self.rect.y += event.rel[1]
                
