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
        
        self.img = pygame.image.load('./media/layouts_and_menus/layout_try.png')
        self.img1=pygame.image.load('./media/layouts_and_menus/layout_try1.png')
        self.img_corner1=pygame.image.load('./media/layouts_and_menus/layout_try_corner_up.png')
        self.img_corner2=pygame.image.load('./media/layouts_and_menus/layout_try_corner_down.png')
        self.img_corner3=pygame.image.load('./media/layouts_and_menus/layout_try_corner_up_dx.png')
        self.img_corner4=pygame.image.load('./media/layouts_and_menus/layout_try_corner_down_dx.png')


        self.rect=pygame.Rect(0,0,Main.screen.get_width(),Main.screen.get_height())
        self.surface=pygame.Surface((Main.screen.get_width(),Main.screen.get_height()))
        self.surface.set_colorkey((0,0,0,0))
        self.blitOnSurface(self.surface)
        
        

    def draw (self):
        
        Main.overlays_layer.blit(self.surface,(0,0))

    def blitOnSurface(self,screen):
        img_height = self.img.get_height()
        img_width = self.img.get_width()
        repetitions_height=self.rect.height//img_height
        counter_h_sx=20
        #draw verticali
        #sx
        for i in range(repetitions_height-2):
            screen.blit(self.img1,(0,counter_h_sx))
            screen.blit(self.img1,(self.rect.width-img_width,counter_h_sx))
            counter_h_sx+=img_height

        #dx
        """ counter_h_dx=20
        for i in range(repetitions_height-2):
            screen.blit(self.img1,(0,counter_h_dx))
            screen.blit(self.img1,(self.rect.width-img_width,counter_h_dx))
            counter_h_dx+=img_height """

        #draw orizzontali
        repetitions_width=self.rect.width//img_width
        #up
        counter_w_up=20
        for i in range(repetitions_width-2):
            screen.blit(self.img,(counter_w_up,0))
            screen.blit(self.img,(counter_w_up,self.rect.height-img_height))
            counter_w_up+=img_width
        #down
        """ counter_w_down=20
        for i in range(repetitions_width-2):
            screen.blit(self.img1,(counter_w_down,0))
            screen.blit(self.img1,(counter_w_down,self.rect.height-img_height))
            counter_w_down+=img_width """

        #corners
        screen.blit(self.img_corner1,(0,0))
        screen.blit(self.img_corner3,(self.rect.width-img_width,0))
        screen.blit(self.img_corner2,(0,self.rect.height-img_height))
        screen.blit(self.img_corner4,(self.rect.width-img_width,self.rect.height-img_height))

        if Main.room.roomNumber is not 2:
            title_rect=pygame.Rect(Main.screen.get_width()/2-Main.screen.get_width()/100*10,20,Main.screen.get_width()/100*20,Main.screen.get_height()/100*5)
            pygame.draw.rect(screen, (133,76,48), title_rect)
            pygame.draw.line(screen, (68,36,52), (title_rect.x,title_rect.y+title_rect.height), (title_rect.x+title_rect.width,title_rect.y+title_rect.height), 2)
            pygame.draw.line(screen, (210,125,44), (title_rect.x,title_rect.y), (title_rect.x+title_rect.width,title_rect.y), 2)
            pygame.draw.line(screen, (210,125,44), (title_rect.x,title_rect.y), (title_rect.x,title_rect.y+title_rect.height), 2)
            pygame.draw.line(screen, (68,36,52), (title_rect.x+title_rect.width,title_rect.y), (title_rect.x+title_rect.width,title_rect.y+title_rect.height), 2)

        
            title_text=Main.font1.render('Hexomunda', True, (210,125,44))
            title_text_shadow=Main.font1.render('Hexomunda', True, (68,36,52))
            title_text=pygame.transform.scale(title_text, (title_rect.width/100*90, title_rect.height/100*80))
            title_text_shadow=pygame.transform.scale(title_text_shadow, (title_rect.width/100*90, title_rect.height/100*80))
            screen.blit(title_text_shadow,(title_rect.x+title_rect.width/2-title_text_shadow.get_width()/2+2,title_rect.y+title_rect.height/2-title_text_shadow.get_height()/2+4))
            screen.blit(title_text,(title_rect.x+title_rect.width/2-title_text.get_width()/2+2,title_rect.y+title_rect.height/2-title_text.get_height()/2+2))
