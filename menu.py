import pygame
import Main
import button
import control
import equipment
from ui_others import *
import os


class Menu:
    def __init__(self,width,height,x,y,type):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect=pygame.Rect(x,y,width,height)
        self.type=type
        self.buttons=[]
        self.startingButtons=[]
        
        self.rect1=pygame.Rect(0,0,100,100)
        # self.img=[middle,up,down,left,right,up_dx,down_dx,up_sx,down_sx]
        self.img=[pygame.image.load('./media/layouts_and_menus/layout_try_middle.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_up.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_down.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_left.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_right.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_up_dx.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_down_dx.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_up_sx.png'),
                  pygame.image.load('./media/layouts_and_menus/layout_try_down_sx.png')] 

        self.surface=pygame.Surface((self.width,self.height))
        
        self.surface.set_colorkey((0,0,0,0))
        
        self.blitOnSurface(self.surface)
        self.originalSurface=self.surface.copy()

    def getRect(self):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        
    def calculateImgDraw(self,screen):
        img_height = self.img[0].get_height()
        img_width = self.img[0].get_width()
        repetitions_height=self.rect.height//img_height
        repetitions_width=self.rect.width//img_width

        
        
        #left, middle and right
        for i in range(repetitions_height):
            
            for j in range(1,repetitions_width):
                screen.blit(self.img[0],(0+(j*img_width),0+(i*img_height)))
            screen.blit(self.img[3],(0,(i*img_height)+0))
            screen.blit(self.img[4],(0+self.rect.width-img_width,(i*img_height)+0))

        #up and down
        for i in range(repetitions_width):
            screen.blit(self.img[1],(0+(i*img_width),0))
            screen.blit(self.img[2],(0+(i*img_width),0+self.rect.height-img_height))

        

        #corners
        screen.blit(self.img[7],(0,0))
        screen.blit(self.img[5],(0+self.rect.width-img_width,0))
        screen.blit(self.img[8],(0,0+self.rect.height-img_height))
        screen.blit(self.img[6],(0+self.rect.width-img_width,0+self.rect.height-img_height))
                
            
    def blitOnSurface(self,screen):
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.calculateImgDraw(screen)
        match self.type: 

            case 'mainmenu':                                        #mainmenu
                self.addButtons()
                

            case 'load game':                                        #loadmenu
                self.addButtons()

            case 'options':                                          #options menu
                self.addButtons()
                
                
            case 'skirmish':                                        #skirmish menu

                
                text=Main.font1.render('Choose the points for players to buy units and equipment', True, (210,125,44))
                text_shadow=Main.font1.render('Choose the points for players to buy units and equipment', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (self.width-20, 16))
                text=pygame.transform.scale(text, (self.width-20, 16))
                screen.blit(text_shadow,(10,9))
                screen.blit(text, (10,8))
                self.addButtons()
                

            case 'unitsInventoryMenu':                              #units inventory menu

                
                text=Main.font1.render('Choose the units to use in game', True, (210,125,44))
                text_shadow=Main.font1.render('Choose the units to use in game', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (self.width/2, 16))
                text=pygame.transform.scale(text, (self.width/2, 16))
                screen.blit(text_shadow,(10,8))
                screen.blit(text, (10,7))
                
                text=Main.font1.render('Click on buy to shop gear', True, (210,125,44))
                text_shadow=Main.font1.render('Click on buy to shop gear', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (200, 16))
                text=pygame.transform.scale(text, (200, 16))
                screen.blit(text_shadow,(self.width-220,20+17))
                screen.blit(text, (self.width-220,20+16))
                self.addButtons()
                
                    
            case 'shop_overlay': #shop overlay
                text=Main.font1.render('Buy equipment for your unit', True, (210,125,44))
                text_shadow=Main.font1.render('Buy equipment for your unit', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (self.width/2, 16))
                text=pygame.transform.scale(text, (self.width/2, 16))
                screen.blit(text_shadow,(10,11))
                screen.blit(text, (10,9))
                

            case 'upi':                                             #unit placing interface
                
                
                text=Main.font1.render('Position your units on the grid by clicking on it', True, (210,125,44))
                text_shadow=Main.font1.render('Position your units on the grid by clicking on it', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (640, 16))
                text=pygame.transform.scale(text, (640, 16))
                screen.blit(text_shadow,(10,8))
                screen.blit(text, (10,7))
                self.addButtons()
            
            case 'pausemenu':
                self.addButtons()

            case 'victory':
                text=Main.font1.render('VICTORY!', True, (210,125,44))
                text_shadow=Main.font1.render('VICTORY!', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (self.width-90, 64))
                text=pygame.transform.scale(text, (self.width-90, 64))
                screen.blit(text_shadow,(self.width/2-text_shadow.get_width()/2,self.height/3-text.get_height()/2+2))
                screen.blit(text, (self.width/2-text_shadow.get_width()/2,self.height/3-text.get_height()/2))
                self.addButtons()

            case 'defeat':
                text=Main.font1.render('DEFEAT', True, (210,125,44))
                text_shadow=Main.font1.render('DEFEAT', True, (68,36,52))
                text_shadow=pygame.transform.scale(text_shadow, (self.width-90, 64))
                text=pygame.transform.scale(text, (self.width-90, 64))
                screen.blit(text_shadow,(self.width/2-text_shadow.get_width()/2,self.height/3-text.get_height()/2+2))
                screen.blit(text, (self.width/2-text_shadow.get_width()/2,self.height/3-text.get_height()/2))
                self.addButtons()


    def draw(self,screen):
        
        screen.blit(self.surface,(self.x,self.y))
        for button in self.buttons:
            button.draw(Main.menu_buttons_layer)

        if self.type == 'unitsInventoryMenu':
            text=Main.font1.render('Points remaining: ' + str(Main.players[0].points), True, (210,125,44))
           
            text=pygame.transform.scale(text, (160, 16))
            
            screen.blit(text, (self.x+10,self.y-40+16))
        
    
    def addButtons(self,relatedObject=None):

        if self.buttons==[]:

            match self.type:  
                case 'mainmenu':  #mainmenu

                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+80,120,80,'mainmenu','play',self))    #play

                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/2-45,120,80,'mainmenu','Load game',self)) #load

                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height-80-80,120,80,'mainmenu','quit',self))    #quit

                case 'options':  #options menu
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+50,120,90,'options','1920x1080',None))   
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+150,120,90,'options','1280x720',None))
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+250,120,90,'options','800x600',None))
                    
                case 'skirmish':  #skirmish menu
                    
                    distance_between_buttons=(self.height/100)*15
                    self.buttons.append(button.Button(self.x+60,self.y+distance_between_buttons,40,40,'skirmish','10',None,'Small'))    #10 punti
                    distance_between_buttons+=(self.height/100)*15
                    self.buttons.append(button.Button(self.x+60,self.y+distance_between_buttons,40,40,'skirmish','15',None,'Small'))    #15 punti
                    distance_between_buttons+=(self.height/100)*15
                    self.buttons.append(button.Button(self.x+60,self.y+distance_between_buttons,40,40,'skirmish','20',None,'Small'))    #20 punti
                    distance_between_buttons+=(self.height/100)*15
                    self.buttons.append(button.Button(self.x+60,self.y+distance_between_buttons,40,40,'skirmish','25',None,'Small'))    #25 punti
                    distance_between_buttons+=(self.height/100)*15
                    self.buttons.append(button.Button(self.x+60,self.y+distance_between_buttons,40,40,'skirmish','60',None,'Small'))    #30 punti
                    
                case 'unitsInventoryMenu':  #units inventory menu
                    increment=20 
                    for unit in Main.units_type_INVENTORY:

                        unit_button=button.Button(self.x+20,self.y+65+increment,unit.img[1].get_width()+10,unit.img[1].get_height()+10,'unitsInventoryMenu',unit.nome,unit)
                        self.buttons.append(unit_button)
                        unit_button.relatedObject=unit

                        add_button=button.Button(self.x+20+unit.img[1].get_width()+20,self.y+65+increment,50,30,'unitsInventoryMenu','add',None)
                        self.buttons.append(add_button)
                        add_button.relatedObject=unit_button
                        
                        increment+=unit.img[1].get_height()+40
                    
                    self.buttons.append(button.Button(self.x+self.width-120,self.y+self.height-120,80,40,'unitsInventoryMenu','next',None))
                    self.startingButtons=self.buttons.copy()

                case 'shop_overlay':  #shop overlay
                    #creo un pulsante per ogni equipaggiamento
                    increment=30
                    close_Shop_Button=button.Button(
                        Main.shop_overlay_menu.x+Main.shop_overlay_menu.width-80,
                        Main.shop_overlay_menu.y+Main.shop_overlay_menu.height-60,
                        64,
                        32,
                        'unitsInventoryMenu_buy',
                        'close',
                        None
                    )
                    scrollbar=Scrollbar(
                                        Main.shop_overlay_menu.x+10,
                                        Main.shop_overlay_menu.y+50,
                                        20,
                                        Main.shop_overlay_menu.height/100*80
                                    )
                    Main.shop_overlay_menu.buttons.append(close_Shop_Button)
                    for equipgroups in equipment.all.values():
                        for equip in equipgroups.keys():
                             
                            if relatedObject.relatedObject.race in equip:

                                
                                equip_button=button.Button(

                                    Main.shop_overlay_menu.x+40,
                                    scrollbar.scroller.y+increment,
                                    Main.shop_overlay_menu.width-(Main.shop_overlay_menu.width/7),
                                    Main.shop_overlay_menu.height/14,
                                    'unitsInventoryMenu_buy',
                                    f'{equip}',
                                    relatedObject,
                                    )
                                equip_button.distanceFromFirstBrotherButton=increment
                                if equip_button.y>Main.shop_overlay_menu.y+Main.shop_overlay_menu.height-120:
                                    scrollbar.color=(0,0,0,120)
                                    scrollbar.scroller.color=(210,125,44,120)
                                    Main.shop_overlay_menu.buttons.append(equip_button)
                                    Main.scrollbars.append(scrollbar)
                                else:
                                    scrollbar.color=(0,0,0,0)
                                    scrollbar.scroller.color=(210,125,44,0)
                                    Main.shop_overlay_menu.buttons.append(equip_button)
                                increment+=70
                                

                    

                case 'upi':        #unit placing interface
                    self.buttons.append(button.Button(self.x+self.width-120,self.y+self.height-120,80,40,'upi','start',None))
                    self.startingButtons=self.buttons.copy()

                case 'pausemenu':  #pause menu

                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/6,120,self.height/8,'pausemenu','Main menu',self))    #main menu
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/6+self.height/8+20,120,self.height/8,'pausemenu','Resume game',self)) #resume
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/6+self.height/4+40,120,self.height/8,'pausemenu','Save game',self)) #save game
                    self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/6+self.height/2+20,120,self.height/8,'mainmenu','quit',self))    #quit


                case 'load game':
                    if os.path.exists('./saved_games'):
                        files = [f for f in os.listdir('./saved_games') if os.path.isfile(os.path.join('./saved_games', f))]
                        increment=0
                        for filee in files:
                            self.buttons.append(button.Button(self.x+self.width/2-60,self.y+self.height/6+increment,120,self.height/8,'load game',filee,self))
                            increment+=80

                case 'victory':
                    self.buttons.append(button.Button(self.x+self.width/2-50,self.y+self.height-70,100,60,'victory','play again',self))

                case 'defeat':
                    self.buttons.append(button.Button(self.x+self.width/2-50,self.y+self.height-70,100,60,'victory','play again',self))
                               
                        
        """ else:
            if self.type=='unitsInventoryMenu':
                for unit in Main.players[0].units_inventory:
                    buy_button=button.Button(unit.center[0]+10,unit.center[1]+50,40,25,'unitsInventoryMenu','buy',unit)
                    if buy_button not in self.buttons:
                        self.buttons.append(buy_button) """
                
                



                    

                    
                
                    





            


              
