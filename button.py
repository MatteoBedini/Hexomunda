import pygame
import Main
import unitt
import equipment
class Button:
    def __init__(self,x,y,width,height,type,description,relatedObject,size='Normal'):

        self.x=x
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

        self.size=size
        self.relatedObject=relatedObject
        self.fakeboy=None
        if self.size=='Small':
            self.img_bg=[pygame.image.load('./media/layouts_and_menus/layout_try_middle.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_left.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_right.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up_dx_empty_round.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down_dx_empty_round.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up_sx_empty_round.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down_sx_empty_round.png')]
        else:
            # self.img=[middle,up,down,left,right,up_dx,down_dx,up_sx,down_sx]
            self.img_bg=[pygame.image.load('./media/layouts_and_menus/layout_try_middle.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_left.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_right.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up_dx_empty.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down_dx_empty.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_up_sx_empty.png'),
                    pygame.image.load('./media/layouts_and_menus/layout_try_down_sx_empty.png')] 
        
        
        

        

    def getRectt(self):

        new_rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.rect=new_rect


    def calculateImgDraw(self,screen):
        img_height = self.img_bg[0].get_height()
        img_width = self.img_bg[0].get_width()
        repetitions_height=self.rect.height//img_height
        repetitions_width=self.rect.width//img_width
        
        if self.size is not 'Small':
            #left, middle and right
            for i in range(repetitions_height):
                screen.blit(self.img_bg[3],(self.x,(i*img_height)+self.y))
                screen.blit(self.img_bg[4],(self.x+self.rect.width-img_width,(i*img_height)+self.y))
                for j in range(1,repetitions_width,-1):
                    screen.blit(self.img_bg[0],(self.x+(j*img_width),self.y+(i*img_height)))

            #up and down
            
            for i in range(repetitions_width):
                screen.blit(self.img_bg[1],(self.x+(i*img_width),self.y))
                screen.blit(self.img_bg[2],(self.x+(i*img_width),self.y+self.rect.height-img_height))


            #corners
            screen.blit(self.img_bg[7],(self.x,self.y))
            screen.blit(self.img_bg[5],(self.x+self.rect.width-img_width,self.y))
            screen.blit(self.img_bg[8],(self.x,self.y+self.rect.height-img_height))
            screen.blit(self.img_bg[6],(self.x+self.rect.width-img_width,self.y+self.rect.height-img_height))
        
        else:
            #left, middle and right
            for i in range(1,repetitions_height,-1):
                screen.blit(self.img_bg[3],(self.x,(i*img_height)+self.y))
                screen.blit(self.img_bg[4],(self.x+self.rect.width-img_width,(i*img_height)+self.y))
                for j in range(1,repetitions_width,-1):
                    screen.blit(self.img_bg[0],(self.x+(j*img_width),self.y+(i*img_height)))

            #up and down
            
            for i in range(1,repetitions_width-1):
                screen.blit(self.img_bg[1],(self.x+(i*img_width),self.y))
                screen.blit(self.img_bg[2],(self.x+(i*img_width),self.y+self.rect.height-img_height))


            #corners
            screen.blit(self.img_bg[7],(self.x,self.y))
            screen.blit(self.img_bg[5],(self.x+self.rect.width-img_width,self.y))
            screen.blit(self.img_bg[8],(self.x,self.y+self.rect.height-img_height))
            screen.blit(self.img_bg[6],(self.x+self.rect.width-img_width,self.y+self.rect.height-img_height))

    def draw(self,screen):
        a=self.x 
        b=self.y
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.calculateImgDraw(screen)

        match self.type:

            #main menu buttons
            case 'mainmenu':
                


                match self.description:
                    case "play":
                        self.img=Main.font1.render('Play', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Play', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-20, self.width-64))
                        screen.blit(self.img_shadow,(a+self.width/2-self.img.get_width()/2,b+self.height/2-self.img.get_height()/2+3))
                        screen.blit(self.img,(a+self.width/2-self.img.get_width()/2,b+self.height/2-self.img.get_height()/2))
                    case "options":
                        self.img=Main.font1.render('Options', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        screen.blit(self.img,(a+self.width/2-self.img.get_width()/2,b+self.height/2-self.img.get_height()/2))
                    case "quit":
                        self.img=Main.font1.render('Exit', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Exit', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.width-64))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-20, self.width-64))
                        screen.blit(self.img_shadow,(a+self.width/2-self.img.get_width()/2,b+self.height/2-self.img.get_height()/2+3))
                        screen.blit(self.img,(a+self.width/2-self.img.get_width()/2,b+self.height/2-self.img.get_height()/2))

                self.mouseCollisionDraw(Main.menu_buttons_layer)

            case 'options':
                
                match self.description:
                    case "1920x1080":
                        self.img=Main.font1.render('1920x1080', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        screen.blit(self.img,(a+8,b+8))
                    case "1280x720":
                        self.img=Main.font1.render('1280x720', True, (210,125,44))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        screen.blit(self.img,(a+8,b+8))
                    #case "800x600":
                        #self.img=Main.font1.render('800x600', True, (210,125,44))
                        #self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        #screen.blit(self.img,(a+8,b+8))

                self.mouseCollisionDraw(Main.menu_buttons_layer)


            #skirmish prepare menu
            case 'skirmish':
                 
                
                match self.description:
                    case "10":
                        self.img=Main.font1.render('10', True, (210,125,44))
                        self.img_shadow=Main.font1.render('10', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        screen.blit(self.img_shadow,(a+8,b+9))
                        screen.blit(self.img,(a+8,b+8))
                    case "15":
                        self.img=Main.font1.render('15', True, (210,125,44))
                        self.img_shadow=Main.font1.render('15', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        screen.blit(self.img_shadow,(a+8,b+9))
                        screen.blit(self.img,(a+8,b+8))
                    case "20":
                        self.img=Main.font1.render('20', True, (210,125,44))
                        self.img_shadow=Main.font1.render('20', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        screen.blit(self.img_shadow,(a+8,b+9))
                        screen.blit(self.img,(a+8,b+8))
                    case "25":
                        self.img=Main.font1.render('25', True, (210,125,44))
                        self.img_shadow=Main.font1.render('25', True, (68,36,52))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        screen.blit(self.img_shadow,(a+8,b+9))
                        screen.blit(self.img,(a+8,b+8))
                    case "60":
                        self.img=Main.font1.render('60', True, (210,125,44))
                        self.img_shadow=Main.font1.render('60', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                        screen.blit(self.img_shadow,(a+8,b+9))
                        screen.blit(self.img,(a+8,b+8))
                self.mouseCollisionDraw(Main.menu_buttons_layer)

            #units inventory menu buttons
            case 'unitsInventoryMenu':

                

                if self.description=='next':
                        self.img=Main.font1.render('Next', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Next', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-20, self.height-10))
                        self.img=pygame.transform.scale(self.img, (self.width-20, self.height-10))
                        screen.blit(self.img_shadow,(a+11,b+8))
                        screen.blit(self.img,(a+11,b+7))

                elif self.description=='add':
                        self.img=Main.font1.render('Add', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Add', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-10))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-10))
                        screen.blit(self.img_shadow,(a+8,b+7))
                        screen.blit(self.img,(a+8,b+6))

                        text=Main.font1.render(f'{self.counter}', True, (210,125,44))
                        text_shadow=Main.font1.render(f'{self.counter}', True, (68,36,52))
                        text_shadow=pygame.transform.scale(text_shadow, (16, 16))
                        text=pygame.transform.scale(text, (16, 16))
                        screen.blit(text_shadow, (self.x+100,self.y+1))
                        screen.blit(text, (self.x+100,self.y))

                elif self.description=='buy':
                        self.img=Main.font1.render('Buy', True, (210,125,44))
                        self.img_shadow=Main.font1.render('Buy', True, (68,36,52))
                        self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-14))
                        self.img=pygame.transform.scale(self.img, (self.width-16, self.height-14))
                        screen.blit(self.img_shadow,(a+8,b+8))
                        screen.blit(self.img,(a+8,b+7))

                for unit in Main.units_type_INVENTORY:
                    if unit.nome==self.description:
                        self.img=[unit.img[0],unit.img[1],unit.img[2],unit.img[3]]
                        for i in self.img:
                            if i!=None:
                                screen.blit(i,(a+self.width/2-i.get_width()/2,b+self.height/2-i.get_height()/2))

                self.mouseCollisionDraw(Main.menu_buttons_layer)

            case 'unitsInventoryMenu_buy':


                if self.description=='close':
                    
                    self.img=Main.font1.render('Close', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Close', True, (68,36,52))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-16, self.height-16))
                    self.img=pygame.transform.scale(self.img, (self.width-16, self.height-16))
                    screen.blit(self.img_shadow,(a+8,b+9))
                    screen.blit(self.img,(a+8,b+8))

                else:
                    increment=20
                    for equipgroups in equipment.all.values():
                        for equip in equipgroups.keys():
                            if equip==self.description:

                                #pygame.draw.rect(screen,(117,113,97),self.rect,border_radius=10)
                                #pygame.draw.rect(screen,(68,36,52),self.rect,3)

                                text1=Main.font1.render(equip, True, (210,125,44))

                                text1=pygame.transform.scale(text1, (self.rect.width - 20, self.rect.height- 28))

                                screen.blit(text1,(self.x+10,self.y+14))
                                if equipgroups[equip][6]!=None:

                                    self.img =pygame.transform.scale(equipgroups[equip][6],(128,128))
                                    screen.blit(self.img,(a+self.width/2-self.img.get_width()/2+130,b+self.height/2-self.img.get_height()/2))
                                increment+=text1.get_height()


                self.mouseCollisionDraw(Main.overlay_menu_buttons_layer)



            #unit placing interface buttons
            case 'upi':


                

                if self.relatedObject!=None:
                    self.img=[self.relatedObject.img[0],self.relatedObject.img[1],self.relatedObject.img[2],self.relatedObject.img[3]]
                    for i in self.img:
                        if i!=None:
                            screen.blit(i,(a+self.width/2-i.get_width()/2,b+self.height/2-i.get_height()/2))

                elif self.description =='start' and self.relatedObject==None:
                    self.img=Main.font1.render('Start', True, (210,125,44))
                    self.img_shadow=Main.font1.render('Start', True, (68,36,52))
                    self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                    self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                    screen.blit(self.img_shadow,(a+5 ,b+6))
                    screen.blit(self.img,(a+5 ,b+5))

                self.mouseCollisionDraw(Main.menu_buttons_layer)

            #end turn button
            case 'endTurn':
                 

                self.img=Main.font1.render('End Turn', True, (210,125,44))
                self.img_shadow=Main.font1.render('End Turn', True, (68,36,52))
                self.img=pygame.transform.scale(self.img, (self.width-10, self.height-10))
                self.img_shadow=pygame.transform.scale(self.img_shadow, (self.width-10, self.height-10))
                screen.blit(self.img_shadow,(a+5 ,b+6))
                screen.blit(self.img,(a+5 ,b+5))

                self.mouseCollisionDraw(Main.menu_buttons_layer)



    #input sul pulsante
    def input(self):
            if self.checkMousecollision()==self:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        match self.type:

                            case 'mainmenu':  #pulsanti nel main menu

                                match self.description:

                                    case "play":
                                        Main.room.roomNumber=3
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

                                            if self.description=='next':
                                                Main.room.roomNumber=2

                                        elif self.description=='add':

                                            if Main.players[0].points>0:
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

                                            increment=0
                                            all_races=[]
                                            orcs=[]
                                            goblins=[]
                                            humans=[]
                                            dwarves=[]
                                            all_races.append(orcs)
                                            all_races.append(goblins)
                                            all_races.append(humans)
                                            all_races.append(dwarves)

                                            for unit in Main.players[0].units_inventory:
                                                if unit.race=='orc':
                                                    all_races[0].append(unit)
                                                elif unit.race=='goblin':
                                                    all_races[1].append(unit)
                                                elif unit.race=='human':
                                                    all_races[2].append(unit)
                                                elif unit.race=='dwarf':
                                                    all_races[3].append(unit)

                                            incrementy=0
                                            for race in all_races:
                                                incrementx=170
                                                for unit in race:
                                                    unit.x=self.x+incrementx
                                                    unit.y=Main.screen.get_height()/3+incrementy+3
                                                    unit.getCenter(unit.x,unit.y)
                                                    incrementx+=unit.img[1].get_height()
                                                incrementy+=unit.img[1].get_height()+25



                                        elif self.description=='buy':
                                            Main.shop_overlay_active=True
                                            Main.shop_overlay_menu.addButtons(relatedObject=self)
                                            




                            case 'unitsInventoryMenu_buy':  #pulsanti nel selezionatore 'buy' unita
                                if self.description=='close':
                                    Main.overlay_menu_box_layer.fill((0, 0, 0, 0))
                                    Main.shop_overlay_active=False
                                    Main.screen.blit(Main.overlay_menu_box_layer,(0,0))
                                    Main.shop_overlay_menu.buttons=[]
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


                                                            if equip in equipment.all[a].keys() and equipment.all[a][equip][5]<=Main.players[0].points:
                                                                if part=='rhand' and unit.animation[0]!=None and unit.animation[0][-4]==True:
                                                                    pass
                                                                elif part=='lhand' and unit.inventory['rhand']!="" and equipment.all[a][self.description][7][-1]==True:
                                                                    pass
                                                                else:
                                                                    Main.players[0].points-=equipment.all[a][equip][5]
                                                                    unit.inventory[part]=self.description
                                                                    unit.applyEquipmentModifiers()


                            case 'upi': #pulsanti nel selezionatore unita

                                        if self.description=='start':
                                            Main.controller.controlGameFases()
                                        else:

                                            mouse_pos = pygame.mouse.get_pos()
                                            self.fakeboy=UnitFake(mouse_pos[0],mouse_pos[1],self.img,self)


                            case 'endTurn': #pulsante di fine turno

                                Main.controller.turnEnd()



    """ def mouseCollisionDraw(self,screen):
         if self.checkMousecollision()==self:
            if self.size == 'Small':
                for img in self.img_bg:
                    pixel_array=pygame.surfarray.array3d(img)
                    color_to_replace=(210,125,44)
                    color_to_replace2=(68,36,52)
                    locked_pixels=[]
                    # Iterate over pixels
                    for y in range(pixel_array.shape[0]):
                        for x in range(pixel_array.shape[1]):
                            pixel = pixel_array[y, x]

                            # Check if the pixel matches color_to_replace2
                            if (pixel == color_to_replace2).all():
                                locked_pixels.append((x, y))  # Store the position of the pixel

                            # Check if the pixel matches color_to_replace
                            elif (pixel == color_to_replace).all():
                                pixel_array[y, x] = color_to_replace2

                    # Modify the locked pixels to color_to_replace
                    for x, y in locked_pixels:
                        pixel_array[y, x] = color_to_replace

            else:
                pygame.draw.line(screen, (68,36,52), (self.x, self.y), (self.x, self.y + self.height-1), 2)  # Lato sinistro 
                pygame.draw.line(screen, (210,125,44), (self.x + self.width-2, self.y), (self.x + self.width-2, self.y + self.height-1), 2)  # Lato destro
                pygame.draw.line(screen, (210,125,44), (self.x, self.y + self.height-2), (self.x + self.width-1, self.y + self.height-2), 2)  # Lato inferiore
                pygame.draw.line(screen, (68,36,52), (self.x, self.y), (self.x + self.width-1, self.y), 2)  # Lato superiore """
    def mouseCollisionDraw(self, screen):
        if self.checkMousecollision() == self:
            if self.size == 'Small':
                text=Main.font1.render(self.description, True, (68, 36, 52))
                
                
                text=pygame.transform.scale(text, (self.width-16, self.height-16))
                screen.blit(text,(self.x+8,self.y+8))

            else:
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
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

