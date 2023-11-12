import Main
import pygame
import math
import random
from hexcell import HexCell
from unitt import Unit
from menu import Menu
from room import Room
from playerr import Player
from control import Control
from button import Button
from inanimate import Inanimated

class Layout:
    def __init__(self):
        self.img = pygame.image.load('./media/layout_try.png')
        self.img1=pygame.image.load('./media/layout_try1.png')
        self.img_corner1=pygame.image.load('./media/layout_try_corner_up.png')
        self.img_corner2=pygame.image.load('./media/layout_try_corner_down.png')

        self.rect=pygame.Rect(0,0,Main.screen.get_width(),Main.screen.get_height())
        

    def draw (self, screen):
        #pygame.draw.rect(screen, (0, 0, 0,0.5), self.rect,20)
        self.calculateImgDraw(Main.layout_layer)

    def calculateImgDraw(self,screen):
        img_height = self.img.get_height()
        img_width = self.img.get_width()
        repetitions_height=self.rect.height//img_height
        counter_h=20
        #draw verticali
        for i in range(repetitions_height-2):
            screen.blit(self.img1,(0,counter_h))
            screen.blit(self.img1,(self.rect.width-img_width,counter_h))
            counter_h+=img_height

        #draw orizzontali
        repetitions_width=self.rect.width//img_width
        counter_w=20
        for i in range(repetitions_width-2):
            screen.blit(self.img,(counter_w,0))
            screen.blit(self.img,(counter_w,self.rect.height-img_height))
            counter_w+=img_width

        #corners
        screen.blit(self.img_corner1,(0,0))
        screen.blit(self.img_corner1,(self.rect.width-img_width,0))
        screen.blit(self.img_corner2,(0,self.rect.height-img_height))
        screen.blit(self.img_corner2,(self.rect.width-img_width,self.rect.height-img_height))