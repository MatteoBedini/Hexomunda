import pygame
import Main
import unitt
import equipment
import copy
import data
class Button:
    def __init__(self,x,y,width,height,type,description,relatedObject,size='Normal'):

        self.x=x
        self.originaly=y
        self.y=y
        self.width=width
        self.height=height
        self.use=None
        self.rect=pygame.Rect((x,y,width,height))
        self.img=None
        self.img_shadow=None
        self.type=type
        self.description=description
        self.counter=0
        self.distanceFromFirstBrotherButton=0

        self.size=size
        self.relatedObject=relatedObject
        self.fakeboy=None
        """ if self.size=='Small':
            self.img_bg=equipment.small_button_bg
        else:
            # self.img=[middle,up,down,left,right,up_dx,down_dx,up_sx,down_sx] """
        self.img_bg=equipment.button_bg
        self.surface=pygame.Surface((self.width,self.height))
        self.visible=True
        self.surface.set_colorkey((0,0,0,0))
        
        self.blitOnSurface()
        self.originalSurface=self.surface.copy()

    def getRectt(self):

        new_rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.rect=new_rect

    def calculateImgDraw(self,screen):
        if self.img_bg !=None:
            img_height = self.img_bg[0].get_height()
            img_width = self.img_bg[0].get_width()
            repetitions_height=self.rect.height//img_height
            repetitions_width=self.rect.width//img_width
            
            """ if self.size is not 'Small': """
            #left, middle and right
            for i in range(repetitions_height):
                
                for j in range(1,repetitions_width):
                    screen.blit(self.img_bg[0],(0+(j*img_width),0+(i*img_height)))
                
                screen.blit(self.img_bg[3],(0,(i*img_height)+0))
                screen.blit(self.img_bg[4],(0+self.rect.width-img_width,(i*img_height)+0))

            #up and down
            
            for i in range(repetitions_width):
                screen.blit(self.img_bg[1],(0+(i*img_width),0))
                screen.blit(self.img_bg[2],(0+(i*img_width),0+self.rect.height-img_height))


            #corners
            screen.blit(self.img_bg[7],(0,0))
            screen.blit(self.img_bg[5],(0+self.rect.width-img_width,0))
            screen.blit(self.img_bg[8],(0,0+self.rect.height-img_height))
            screen.blit(self.img_bg[6],(0+self.rect.width-img_width,0+self.rect.height-img_height))
            
            """ else:
                #left, middle and right
                for i in range(1,repetitions_height,-1):
                    screen.blit(self.img_bg[3],(0,(i*img_height)+0))
                    screen.blit(self.img_bg[4],(0+self.rect.width-img_width,(i*img_height)+0))
                    for j in range(1,repetitions_width,-1):
                        screen.blit(self.img_bg[0],(0+(j*img_width),0+(i*img_height)))

                #up and down
                
                for i in range(1,repetitions_width-1):
                    screen.blit(self.img_bg[1],(0+(i*img_width),0))
                    screen.blit(self.img_bg[2],(0+(i*img_width),0+self.rect.height-img_height))


                #corners
                screen.blit(self.img_bg[7],(0,0))
                screen.blit(self.img_bg[5],(0+self.rect.width-img_width,0))
                screen.blit(self.img_bg[8],(0,0+self.rect.height-img_height))
                screen.blit(self.img_bg[6],(0+self.rect.width-img_width,0+self.rect.height-img_height)) """

    def blitOnSurface(self):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.calculateImgDraw(self.surface)

        match self.type:

            #main menu buttons
            case 'mainmenu':
                


                match self.description:
                    case "play":
                        self.img=Main.font1.render('New game', True, (210,125,44))
                        self.img_shadow=Main.font1.render('New game', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-20, self.width-64))
                        self.surface.blit(self.img_shadow,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2+3))
                        self.surface.blit(self.img,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2))
                    case "Load game":
                        self.img=Main.font1.render('Load game', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        self.surface.blit(self.img,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2))
                    case "quit":
                        self.img=Main.font1.render('Exit', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Exit', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-20, self.width-64))
                        self.surface.blit(self.img_shadow,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2+3))
                        self.surface.blit(self.img,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2))

            case 'options':
                

                
                match self.description:
                    case "1920x1080":
                        self.img=Main.font1.render('1920x1080', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.surface.blit(self.img,(8,8))
                    case "1280x720":
                        self.img=Main.font1.render('1280x720', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.surface.blit(self.img,(8,8))
                    #case "800x600":
                        #self.img=Main.font1.render('800x600', True, (210,125,44))
                        #self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        #self.surface.blit(self.img,(8,8))

            #skirmish prepare menu
            case 'skirmish':
                match self.description:
                    case "10":
                        self.img=Main.font1.render('10', True, (210,125,44))
                        self.img_shadow=Main.font1.render('10', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.surface.blit(self.img_shadow,(8,9))
                        self.surface.blit(self.img,(8,8))
                    case "15":
                        self.img=Main.font1.render('15', True, (210,125,44))
                        self.img_shadow=Main.font1.render('15', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.surface.blit(self.img_shadow,(8,9))
                        self.surface.blit(self.img,(8,8))
                    case "20":
                        self.img=Main.font1.render('20', True, (210,125,44))
                        self.img_shadow=Main.font1.render('20', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.surface.blit(self.img_shadow,(8,9))
                        self.surface.blit(self.img,(8,8))
                    case "25":
                        self.img=Main.font1.render('25', True, (210,125,44))
                        self.img_shadow=Main.font1.render('25', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.surface.blit(self.img_shadow,(8,9))
                        self.surface.blit(self.img,(8,8))
                    case "60":
                        self.img=Main.font1.render('60', True, (210,125,44))
                        self.img_shadow=Main.font1.render('60', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.surface.blit(self.img_shadow,(8,9))
                        self.surface.blit(self.img,(8,8))
                

            #units inventory menu buttons
            case 'unitsInventoryMenu':

                if self.description=='next':
                        self.img=Main.font1.render('Next', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Next', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.img.get_width()/3, self.height-10))
                        self.img=pygame.transform.scale(self.img, (self.img.get_width()/3, self.height-10))
                        self.surface.blit(self.img_shadow,(self.width/2-self.img.get_width()/2,8))
                        self.surface.blit(self.img,(self.width/2-self.img.get_width()/2,7))

                elif self.description=='add':
                        self.img=Main.font1.render('+', True, (210,125,44))
                        self.img_shadow=Main.font1.render('+', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.img.get_width()/3, self.img.get_height()/3))
                        self.img=pygame.transform.scale(self.img, (self.img.get_width()/3, self.img.get_height()/3))
                        self.surface.blit(self.img_shadow,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2+2))
                        self.surface.blit(self.img,(self.width/2-self.img.get_width()/2,self.height/2-self.img.get_height()/2))

                        text=Main.font1.render(f'{self.counter}', True, (210,125,44))
                        text_shadow=Main.font1.render(f'{self.counter}', True, (68,36,52))
                        text_shadow=pygame.transform.scale(text_shadow, (16, 16))
                        text=pygame.transform.scale(text, (16, 16))
                        self.surface.blit(text_shadow, (self.x+100,self.y+1))
                        self.surface.blit(text, (self.x+100,self.y))

                elif self.description=='buy':
                        self.img=Main.font1.render('Buy', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Buy', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-14))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-14))
                        self.surface.blit(self.img_shadow,(8,8))
                        self.surface.blit(self.img,(8,7))

                for unit in Main.units_type_INVENTORY:
                    if unit.nome==self.description:
                        self.img=[unit.img[0],unit.img[1],unit.img[2],unit.img[3]]
                        for i in self.img:
                            if i!=None:
                                self.surface.blit(i,(self.width/2-i.get_width()/2,self.height/2-i.get_height()/2))
                        unit_name=Main.font1.render(f'{unit.nome}', True, (210,125,44))
                        unit_name_shadow=Main.font1.render(f'{unit.nome}', True, (68,36,52))
                        unit_name_shadow=pygame.transform.scale(unit_name_shadow, (unit_name.get_width()/3.5, self.height/3))
                        unit_name=pygame.transform.scale(unit_name, (unit_name.get_width()/3.5, self.height/3))
                        self.surface.blit(unit_name_shadow,(self.width+10,self.height-unit_name_shadow.get_height()-8))
                        self.surface.blit(unit_name,(self.width+10,self.height-unit_name.get_height()-10))

                

            case 'unitsInventoryMenu_buy':


                if self.description=='close':
                    
                    self.img=Main.font1.render('Close', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Close', True, (68,36,52))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                    self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                    self.surface.blit(self.img_shadow,(8,9))
                    self.surface.blit(self.img,(8,8))

                else:
                   
                    for equipgroups in equipment.all.values():
                        for equip in equipgroups.keys():
                            if self.description == equip:

                                #pygame.draw.rect(self.surface,(117,113,97),self.rect,border_radius=10)
                                #pygame.draw.rect(self.surface,(68,36,52),self.rect,3)
                                substring_to_remove=self.relatedObject.relatedObject.race

                                string=copy.deepcopy(self.description)
                                string=string.replace(substring_to_remove,'')
                                equip_name=Main.font1.render(string, True, (210,125,44))
                                equip_name_shadow=Main.font1.render(string, True, (68,36,52))
                                equip_name_shadow=pygame.transform.scale(equip_name_shadow, (equip_name.get_width()/4, self.rect.height- 26))
                                equip_name=pygame.transform.scale(equip_name, (equip_name.get_width()/4, self.rect.height- 26))

                                

                                """ self.surface.blit(equip_name_shadow,(10,16)) """
                                self.surface.blit(equip_name,(10,14))
                                if equipgroups[equip][6]!=None:
                                    
                                    self.img =equipgroups[equip][6]
                                    self.surface.blit(self.img,(self.width/3 ,self.height/2-self.img.get_height()/2))


                                equip_cost=Main.font1.render(f'points cost: {equipgroups[equip][5]}', True, (210,125,44))
                                equip_cost_shadow=Main.font1.render(f'points cost: {equipgroups[equip][5]}', True, (68,36,52))
                                equip_cost_shadow=pygame.transform.scale(equip_cost_shadow, (equip_cost.get_width()/4, equip_cost.get_height()/4))
                                equip_cost=pygame.transform.scale(equip_cost, (equip_cost.get_width()/4, equip_cost.get_height()/4))
                                
                                """ self.surface.blit(equip_cost_shadow,(self.width/3+self.img.get_width(),8)) """
                                self.surface.blit(equip_cost,(self.width/3+self.img.get_width(),6))

                                equip_stats=Main.font1.render(f'hp : +{equipgroups[equip][0]}  atk : +{equipgroups[equip][1]}  range : +{equipgroups[equip][4]}', True, (210,125,44))
                                equip_stats_shadow=Main.font1.render(f'hp : +{equipgroups[equip][0]}  atk : +{equipgroups[equip][1]}  range : +{equipgroups[equip][4]}', True, (68,36,52))
                                equip_stats_shadow=pygame.transform.scale(equip_stats_shadow, (equip_stats.get_width()/4, equip_stats.get_height()/4))
                                equip_stats=pygame.transform.scale(equip_stats, (equip_stats.get_width()/4, equip_stats.get_height()/4))

                                """ self.surface.blit(equip_stats_shadow,(self.width/3+self.img.get_width(),self.height-18)) """
                                self.surface.blit(equip_stats,(self.width/3+self.img.get_width(),self.height-20))

            #unit placing interface buttons
            case 'upi':

                """ if self.relatedObject!=None:
                    self.img=[self.relatedObject.img[0],self.relatedObject.img[1],self.relatedObject.img[2],self.relatedObject.img[3]]
                    for i in self.img:
                        if i!=None:
                            self.surface.blit(i,(self.width/2-i.get_width()/2,self.height/2-i.get_height()/2)) """

                if self.description =='start' and self.relatedObject==None:
                    self.img=Main.font1.render('Start', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Start', True, (68,36,52))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                    self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                    self.surface.blit(self.img_shadow,(5 ,6))
                    self.surface.blit(self.img,(5 ,5))

            case 'pausemenu':
                if self.description == 'Main menu':
                    self.img=Main.font1.render('Main menu', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Main menu', True, (68,36,52))
                    self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                    self.surface.blit(self.img_shadow,(5 ,6))
                    self.surface.blit(self.img,(5 ,5))  
                elif self.description == 'Resume game':
                    self.img=Main.font1.render('Resume game', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Resume game', True, (68,36,52))
                    self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                    self.surface.blit(self.img_shadow,(5 ,6))
                    self.surface.blit(self.img,(5 ,5))
                elif self.description == 'Save game':
                    self.img=Main.font1.render('Save game', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Save game', True, (68,36,52))
                    self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                    self.surface.blit(self.img_shadow,(5 ,6))
                    self.surface.blit(self.img,(5 ,5))
            #end turn button
            case 'endTurn':
                self.img=Main.font1.render('End Turn', True, (210,125,44))
                self.img_shadow=Main.font1.render('End Turn', True, (68,36,52))
                self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                self.surface.blit(self.img_shadow,(5 ,6))
                self.surface.blit(self.img,(5 ,5))

            case 'victory':
                self.img=Main.font1.render('Play again', True, (210,125,44))
                self.img_shadow=Main.font1.render('Play again', True, (68,36,52))
                self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                self.surface.blit(self.img_shadow,(5 ,6))
                self.surface.blit(self.img,(5 ,5))

            case 'load game':
                new_string=str(self.description).replace('.txt','')
                new_new_string=new_string.replace('_',' ')
                new_string=new_new_string
                self.img=Main.font1.render(f'{new_string}', True, (210,125,44))
                self.img_shadow=Main.font1.render(f'{new_string}', True, (68,36,52))
                self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                self.surface.blit(self.img_shadow,(5 ,6))
                self.surface.blit(self.img,(5 ,5))
                                
    def draw(self,screen):
        screen.blit(self.surface,(self.x,self.y))
        if self.visible==True:
           
            if self.type=='upi':
                if self.relatedObject!=None:
                    self.img=[self.relatedObject.img[0],self.relatedObject.img[1],self.relatedObject.img[2],self.relatedObject.img[3]]
                    for i in self.img:
                        if i!=None:
                            screen.blit(i,(self.x+self.width/2-i.get_width()/2,self.y+self.height/2-i.get_height()/2))  
            self.mouseCollisionDraw(screen)

    def otherEvents(self):
        match self.type:
            case 'unitsInventoryMenu_buy':
                if self.description=='close':
                    pass
                else:
                    for scrollbar in Main.scrollbars:
                        if scrollbar.scroller.dragging==True:
                            difference=scrollbar.scroller.rect.y-scrollbar.scroller.startingy
                            self.getRectt()
                            self.y=scrollbar.scroller.startingy-difference+self.distanceFromFirstBrotherButton
                        if self.y>Main.shop_overlay_menu.y+Main.shop_overlay_menu.height-120 or self.y<Main.shop_overlay_menu.y+40:
                            self.surface.fill((0,0,0,0))
                            self.visible=False

                        else:   
                            self.surface=self.originalSurface.copy()
                            self.visible=True

    def input(self):
            
            if self.checkMousecollision()==self and self.visible==True:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        match self.type:

                            case 'mainmenu':  #pulsanti nel main menu

                                match self.description:

                                    case "play":

                                        for player in Main.players:
                                            player.points=0
                                            player.units_inventory=[]
                                            player.units=[]
                                            player.ai_selection_ended=False

                                        Main.inanimated_in_game=[]
                                        Main.deadunits=[]
                                        Main.controller.gameFase=0  
                                        Main.controller.selectedd = None
                                        Main.controller.ai_selected=None
                                        Main.controller.actingUnit = None
                                        Main.controller.turn = 1
                                        Main.controller.actingPlayer = 0 
                                        Main.unitsInventoryMenu.buttons=[]
                                        Main.unitsInventoryMenu.addButtons()

                                        for button in Main.unitsInventoryMenu.buttons:
                                            print(button.description)
                                        
                                        Main.room.roomNumber=3

                                    case "Load game":
                                        Main.load_game_menu.buttons=[]
                                        Main.load_game_menu.addButtons()
                                        Main.room.roomNumber=7
                                    case "options":
                                        
                                        Main.room.roomNumber=4
                                    case "quit":
                                        Main.running=False

                            case 'options':
                                match self.description:
                                    case "1920x1080":

                                        Main.screen=pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)


                                    case "1280x720":
                                        Main.screen=pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
                                        """ Main.resizable_layer_x+=1280-Main.controller.screenSize[0]+320
                                        Main.resizable_layer_y+=720-Main.controller.screenSize[1]+180
                                        Main.controller.screenSize=(1280,720)
                                        Main.controller.AdaptObjectsToScreenSize() """



                                    #case "800x600":
                                        #Main.screen=pygame.display.set_mode((800,600),pygame.RESIZABLE)

                            case 'skirmish':
                                
                                for player in Main.players:
                                    match self.description:
                                        case "10":
                                            player.points=10
                                        case "15":
                                            player.points=15
                                        case "20":
                                            player.points=20
                                        case "25":
                                            player.points=25
                                        case "60":
                                            player.points=60

                                Main.room.roomNumber=1

                              

                            case 'unitsInventoryMenu':  #pulsanti nel selezionatore unita

                                    if self.description=='next':

                                        
                                        Main.room.roomNumber=2

                                        
                                        

                                    elif self.description=='add':
                                        Main.all_races=[[],[],[],[]]
                                        Main.menus[2].buttons=Main.menus[2].startingButtons.copy()
                                        Main.menus[1].buttons=Main.menus[1].startingButtons.copy()
                                        if Main.players[0].points-5>=0:
                                            a=self.relatedObject.relatedObject

                                            new_unit=unitt.Unit(a.ai,a.id,a.nome,a.race) #creo una nuova unita uguale alla unita dell'inventario nel Main
                                            for i in new_unit.img:
                                                for j in a.img:
                                                    for d in range(3):
                                                        if new_unit.img[d]==i and a.img[d]==j:
                                                            i=j
                                            Main.players[0].units_inventory.append(new_unit) #e poi la assegno all' inventario del giocatore
                                            Main.players[0].points-=5
                                            

                                            self.counter+=1

                                        increment=20
                                        for unit in Main.players[0].units_inventory:
                                            if unit.race=='orc':
                                                Main.all_races[0].append(unit)
                                            elif unit.race=='goblin':
                                                Main.all_races[1].append(unit)
                                            elif unit.race=='human':
                                                Main.all_races[2].append(unit)
                                            elif unit.race=='dwarf':
                                                Main.all_races[3].append(unit)
                                            menu=Main.menus[2] #upi
                                            menu.buttons.append(Button(menu.x+increment,menu.y+40,unit.img[1].get_width()+10,unit.img[1].get_height()+10,'upi',unit.nome,unit))
                                            increment+=unit.img[1].get_width()+20
                                                
                                        


                                        incrementy=0
                                        for race in Main.all_races:
                                            incrementx=170
                                            for unit in race:
                                                
                                                unit.x=self.x+incrementx
                                                unit.y=Main.screen.get_height()/3+incrementy+3
                                                unit.getCenter(unit.x,unit.y)
                                                incrementx+=unit.img[1].get_height()
                                                menu=Main.menus[1] #unitsInventoryMenu
                                                        
                                                buy_button=Button(unit.center[0]+10,unit.center[1]+50,40,25,'unitsInventoryMenu','buy',unit)
                                                menu.buttons.append(buy_button)
                                                    
                                            incrementy+=unit.img[1].get_height()+25



                                    elif self.description=='buy':
                                        Main.shop_overlay_active=True
                                        Main.shop_overlay_menu.addButtons(relatedObject=self)
                                        




                            case 'unitsInventoryMenu_buy':  #pulsanti nel selezionatore 'buy' unita
                                if self.description=='close':
                                    """ Main.overlay_menu_box_layer.fill((0, 0, 0, 0)) """
                                    Main.shop_overlay_active=False
                                    """ Main.screen.blit(Main.overlay_menu_box_layer,(0,0)) """
                                    Main.shop_overlay_menu.buttons=[]
                                    Main.scrollbars=[]
                                    #Main.shop_overlay_buttons=[]




                                #assegno all' unità il pezzo di equipaggiamento richiesto e rimuovo i punti dal giocatore
                                #inoltre avvio l'applyfyEquipmentModifiers sull'unità in questione
                                else:
    
                                        unit=self.relatedObject.relatedObject

                                        for part in unit.inventory.keys():
                                            for groups in equipment.all.values():

                                                for equip in groups.keys():

                                                    if self.description==equip:

                                                        for a in equipment.all.keys():
                                                            if a==part:


                                                                if equip in equipment.all[a].keys() and Main.players[0].points-equipment.all[a][equip][5]>=0:
                                                                    #se l'unita ha un arma a due mani nella lhand passo
                                                                    if part=='rhand' and unit.animation[0]!=None and unit.animation[0][-4]==True:
                                                                        pass
                                                                    #se l'unita ha un arma a due mani nella rhand passo
                                                                    elif part=='lhand' and unit.animation[3]!=None and unit.animation[3][-4]==True:
                                                                        pass
                                                                    elif part=='lhand' and unit.inventory['rhand']!="" and equipment.all[a][self.description][7][-1]==True:
                                                                        pass
                                                                    elif part=='rhand' and unit.inventory['lhand']!="" and equipment.all[a][self.description][7][-1]==True:
                                                                        pass

                                                                    else:
                                                                        Main.players[0].points-=equipment.all[a][equip][5]
                                                                        unit.inventory[part]=self.description
                                                                        unit.applyEquipmentModifiers()


                            case 'upi': #pulsanti nel selezionatore unita

                                        if self.description=='start':
                                            Main.controller.controlGameFases()
                                        else:
                                            if self.relatedObject!=None:
                                               
                                                mouse_pos = pygame.mouse.get_pos()
                                                self.fakeboy=UnitFake(mouse_pos[0],mouse_pos[1],self.img,self)
                                                self.surface.fill((0,0,0,0))
                                                
                                                self.img=[]
                                                self.calculateImgDraw(self.surface)

                            case 'pausemenu':

                                if self.description == 'Main menu':
                                    Main.room.roomNumber=0
                                elif self.description == 'Resume game':
                                    Main.room.roomNumber=2
                                elif self.description == 'Save game':
                                    data.save()

                            case 'load game':
                                for player in Main.players:
                                        player.points=0
                                        player.units_inventory=[]
                                        player.units=[]
                                        player.ai_selection_ended=False

                                Main.controller.gameFase=0  
                                Main.controller.selectedd = None
                                Main.controller.ai_selected=None
                                Main.controller.actingUnit = None
                                Main.controller.turn = 1
                                Main.controller.actingPlayer = 0 
                                Main.unitsInventoryMenu.buttons=[]
                                Main.unitsInventoryMenu.addButtons()
                                data.load(self.description)
                        
                            case 'endTurn': #pulsante di fine turno

                                Main.controller.turnEnd()

                            case 'victory': #pulsante di fine partita

                                Main.room.roomNumber=0

                            case 'defeat': #pulsante di fine partita

                                Main.room.roomNumber=0

    def mouseCollisionDraw(self, screen):
        if self.checkMousecollision() == self:
            """ if self.size == 'Small':
                text=Main.font1.render(self.description, True, (68, 36, 52))
                
                
                text=pygame.transform.scale(text, (self.width-16, self.height-16))
                screen.blit(text,(self.x+8,self.y+8))

            else: """
            # Draw lines for the larger size
            pygame.draw.line(screen, (68, 36, 52), (self.x, self.y), (self.x, self.y + self.height - 1), 2)  # Lato sinistro 
            pygame.draw.line(screen, (210, 125, 44), (self.x + self.width - 2, self.y), (self.x + self.width - 2, self.y + self.height - 1), 2)  # Lato destro
            pygame.draw.line(screen, (210, 125, 44), (self.x, self.y + self.height - 2), (self.x + self.width - 1, self.y + self.height - 2), 2)  # Lato inferiore
            pygame.draw.line(screen, (68, 36, 52), (self.x, self.y), (self.x + self.width - 1, self.y), 2)  # Lato superiore

    def checkMousecollision(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rect.collidepoint(mouse_pos[0], mouse_pos[1])

        ):

            return self
        else:
            return None

    def moveFakeBoy(self):
        if self.fakeboy!=None:
            self.fakeboy.move()



class UnitFake:

    def __init__(self,x,y,img,parentButton):
        self.x=x
        self.y=y
        self.img=img
        self.parentButton=parentButton

    def move(self):
        self.x=pygame.mouse.get_pos()[0]
        self.y=pygame.mouse.get_pos()[1]
        self.draw()
        self.place()

    def draw(self):
        for i in self.img:
            if i !=None:
                Main.menu_buttons_layer.blit(i,(self.x,self.y))

    def place(self):
        for cell in Main.hex_cells:
            if cell.checkHexMousecollision()==cell and cell.col in range(0,3) and cell.occupied==False:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.parentButton.relatedObject!=None:
                        a=self.parentButton.relatedObject
                        new_unit=unitt.Unit(a.ai,a.id,a.nome,a.race) #creo una nuova unita uguale alla unita dell'inventario del player
                        #copio l'equipaggiamento dell'unita dell'inventario
                        for piece in a.inventory.keys():
                             for part in new_unit.inventory.keys():
                                  if piece==part:

                                    new_unit.inventory[part]=a.inventory[piece]



                        print(new_unit.inventory)

                        new_unit.applyEquipmentModifiers()
                        for i in new_unit.img:
                            for j in a.img:
                                for d in range(3):
                                    if new_unit.img[d]==i and a.img[d]==j:
                                        i=j


                        Main.players[0].units.append(new_unit) #e poi la assegno alle unita giocanti del player
                        new_unit.x=cell.center[0]
                        new_unit.y=cell.center[1]
                        new_unit.getCenter(new_unit.x,new_unit.y)
                        new_unit.getParentCell()
                        new_unit.createMask()
                        new_unit.id=Main.players[0].units.index(new_unit)
                        #new_unit.img=pygame.transform.scale(new_unit.img, (new_unit.img.get_width()*2, new_unit.img.get_height()*2))
                        self.parentButton.fakeboy=None
                        self.parentButton.relatedObject=None
                        cell.occupied=True

                                            
            
            

    #input sul pulsante

                                
        

