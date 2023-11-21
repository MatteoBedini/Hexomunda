""" import pygame
import math

from hexcell import HexCell

from menu import Menu
import button
from room import Room
from player import Player """

import random
import Main 
import pygame
from inanimate import Inanimated
import math
import menu
import button
# classe controllore del gioco
# ----------------------------------------------------------------------------------------------------------------------------------------------------
class Control:
    def __init__(self):
        self.selectedd = None
        self.ai_selected=None
        self.turn = 1
        self.actingPlayer = 0   #turno giocatore
        self.gameFase=0
        self.maxgameFase=1      #unità che sta effettuando un movimento grafico
        self.actingUnit=None
        self.overlayedUnit=None
        self.overlayedUnit_overlay=None
        self.screenSize=[Main.width,Main.height]
        

        
    def controlGameFases(self):
        self.gameFase+=1
        if self.gameFase>self.maxgameFase:
            self.gameFase=self.maxgameFase
       

    # check per segnare quali celle sono occupate
    def checkOccupiedCells(self):
        for cell in Main.hex_cells:
            cell.occupied = False
            for player in Main.players:
                for unit in player.units:
                    if (
                        unit.rectForParent.collidepoint(cell.center[0], cell.center[1])
                        == True
                    ):
                        cell.occupied = True
                        """ print('1 cell occupied +') """
            for objectt in Main.inanimated_in_game:
                if (
                    objectt.rectForParent.collidepoint(cell.center[0], cell.center[1])
                    == True
                ):
                    cell.occupied = True

    # attivazione unit del giocatore attivo
    def unitStart(self):
        for x in range(len(Main.players)):
            if self.actingPlayer == x:
                for unit in Main.players[x].units:
                    if unit.activated==False:
                        unit.activated = True
                        #print('activated boy')
                        #print(unit)

    # gestione fine turno
    def turnEnd(self):
        self.selectedd = None
        for player in Main.players:
            for unit in player.units:
                unit.movepts = unit.totmovepts
                unit.atkpts = unit.totatkpts
                unit.activated = False
                unit.selected = False
                unit.aiFinishedTurn=False
                self.ai_selected = None
        
        if (
            self.actingPlayer > len(Main.players)-2 
        ):  # esempio len è 2,  acting players 0,1 se siamo a 0 fa next se siamo a 1, 2-2=0, 1>0 'si riparte'
            self.actingPlayer = 0
            print("si riparte")
        else:
            self.actingPlayer += 1
            print("next: ", self.actingPlayer)
        self.checkOccupiedCells()

        

    #overlay informativo al clic su un oggetto
    def createObjectOverlay(self,unit):
        if unit.rectMask.collidepoint(pygame.mouse.get_pos()):
            self.overlayedUnit_overlay=pygame.image.load("media/ObjectInfo_overlay.png")
            self.overlayedUnit=unit
        elif self.overlayedUnit!=None and not self.overlayedUnit.rectMask.collidepoint(pygame.mouse.get_pos()):
            self.overlayedUnit=None
                            

    #draw del suddetto overlay
    def drawObjectOverlay(self,screen):
        
        if Main.zoom <2:
            zoomey=2
            
        else:
            
            zoomey=1

        if self.overlayedUnit!=None:
            inventory=pygame.image.load("media/ObjectInfo_inventory.png")
            x=20
            y=Main.screen.get_height()-self.overlayedUnit_overlay.get_height()-20
            
            
            screen.blit(self.overlayedUnit_overlay,(x,y))
            for i in self.overlayedUnit.img:
                if i!=None:
                    equipment_image=i
                    equipment_image=pygame.transform.scale(equipment_image,(i.get_width()*zoomey,i.get_height()*zoomey))
                    screen.blit(equipment_image,(x+self.overlayedUnit_overlay.get_width()/100*50-equipment_image.get_width()/2,y+self.overlayedUnit_overlay.get_height()/100*50-equipment_image.get_height()/2))
                    
            screen.blit(inventory,(20,Main.screen.get_height()-inventory.get_height()-20-self.overlayedUnit_overlay.get_height()))
            inventory_x=20
            inventory_y=Main.screen.get_height()-inventory.get_height()-20-self.overlayedUnit_overlay.get_height()

            #head
            if self.overlayedUnit.img[2]!=None:
                p=self.overlayedUnit.img[2]
                p=pygame.transform.scale(p,(p.get_width()*zoomey,p.get_height()*zoomey))
                screen.blit(p, (inventory_x+inventory.get_width()/100*50-p.get_width()/2,inventory_y+inventory.get_height()/100*20-p.get_height()/2))

            #weapon
            if self.overlayedUnit.img[0]!=None:
                p=self.overlayedUnit.img[0]
                p=pygame.transform.scale(p,(p.get_width()*zoomey,p.get_height()*zoomey))
                screen.blit(p, (inventory_x+inventory.get_width()/100*80-p.get_width()/2, inventory_y+inventory.get_height()/100*50-p.get_height()/2))

            #shield
            if self.overlayedUnit.img[3]!=None:
                p=self.overlayedUnit.img[3]
                p=pygame.transform.scale(p,(p.get_width()*zoomey,p.get_height()*zoomey))
                screen.blit(p, (inventory_x+inventory.get_width()/100*20-p.get_width()/2, inventory_y+inventory.get_height()/100*50-p.get_height()/2))

            #body
            if self.overlayedUnit.img[1]!=None:
                p=self.overlayedUnit.img[1]
                p=pygame.transform.scale(p,(p.get_width()*zoomey,p.get_height()*zoomey))
                screen.blit(p, (inventory_x+inventory.get_width()/100*50-p.get_width()/2, inventory_y+inventory.get_height()/100*50-p.get_height()/2))

            hp=Main.font.render('Hp:', True, (210,125,44))
            hp_shadow=Main.font.render('Hp:', True, (68,36,52))
            hp_shadow=pygame.transform.scale(hp_shadow, (hp_shadow.get_width()/2, hp_shadow.get_height()/2))
            hp=pygame.transform.scale(hp, (hp.get_width()/2, hp.get_height()/2))
            screen.blit(hp_shadow, (x+20, y+1+(self.overlayedUnit_overlay.get_height()/100*80)))
            screen.blit(hp, (x+20, y+(self.overlayedUnit_overlay.get_height()/100*80)))

            atk=Main.font.render('Attack:'+str(self.overlayedUnit.atk), True, (210,125,44))
            atk_shadow=Main.font.render('Attack:'+str(self.overlayedUnit.atk), True, (68,36,52))
            atk_shadow=pygame.transform.scale(atk_shadow, (atk_shadow.get_width()/2, atk_shadow.get_height()/2))
            atk=pygame.transform.scale(atk, (atk.get_width()/2, atk.get_height()/2))
            screen.blit(atk_shadow, (x+self.overlayedUnit_overlay.get_width()-atk_shadow.get_width()-20, y+(self.overlayedUnit_overlay.get_height()/100*10)))
            screen.blit(atk, (x+self.overlayedUnit_overlay.get_width()-atk.get_width()-20, y+(self.overlayedUnit_overlay.get_height()/100*10)))

            name=Main.font.render('Name:'+str(self.overlayedUnit.nome), True, (210,125,44))
            name_shadow=Main.font.render('Name:'+str(self.overlayedUnit.nome), True, (68,36,52))
            name_shadow=pygame.transform.scale(name_shadow, (name_shadow.get_width()/2, name_shadow.get_height()/2))
            name=pygame.transform.scale(name, (name.get_width()/2, name.get_height()/2))
            screen.blit(name_shadow, (x+20, y+(self.overlayedUnit_overlay.get_height()/100*10)))
            screen.blit(name, (x+20, y+(self.overlayedUnit_overlay.get_height()/100*10)))

            if zoomey==2:
                self.overlayedUnit.drawHpBar(screen,80,15,x+30+hp.get_width(),y-1+(self.overlayedUnit_overlay.get_height()/100*80)+Main.resizable_layer_y)
            else:
                self.overlayedUnit.drawHpBar(screen,80/2,15,x+30+hp.get_width()-32,y-1+(self.overlayedUnit_overlay.get_height()/100*80)+Main.resizable_layer_y)
            

    # elimino unità morte dall'array units e le metto nell'array deadunits
    def kill(self, unit):
        Main.deadunits.append(unit)
        for player in Main.players:
            for x in player.units:
                if unit == x:
                    player.units.remove(unit)

    #ai_ posizionamento unità all'inizio della partita
    def ai_pos(self):

        for unit in Main.players[1].units:
            if unit.ai == True:
                viablecells=[]

                for cell in Main.hex_cells:
                    if cell.col in range(Main.COL_COUNT-3,Main.COL_COUNT):  #LE CELLE IN CUI L'AI POSSONO POSIZIONARE LE UNITA SONO NELLA META CAMPO AVVERSARIA
                        viablecells.append(cell)
                
                randomcell=viablecells[random.randrange(0,len(viablecells)-1)]

                if randomcell.occupied==False and unit.parentcell==None:

                    unit.x = randomcell.center[0]
                    unit.y = randomcell.center[1]
                    unit.getCenter(unit.x,unit.y)
                    unit.getParentCell()
                    #print (randomcell)
                    #print(f'{unit.x},{unit.y},{unit.id},{unit.nome}')
                    unit.createMask()
                    randomcell.occupied = True
                    
    # ai_selezione unità
    def ai_select_control(self):
        for player in Main.players:
            if Main.controller.actingPlayer==Main.players.index(player) and player.ai == True:
                
                for x in range(len(player.units)):
                    if (
                        player.units[x].ai == True
                        
                        and player.units[x].aiFinishedTurn == False
                        and player.units[x].activated == True
                    ):
                        
                        if x - 1 >= 0:
                            
                            if player.units[x - 1].aiFinishedTurn == True:
                                self.ai_selected= player.units[x]
                                print(f'ai seleziona {self.ai_selected}')
                        elif x == 0:
                            self.ai_selected= player.units[x]
                            print(f'ai seleziona {self.ai_selected}')
                    else:
                        self.ai_selected=None


    def InanimatePlace(self):
         #faccio piazzare all' ai degli oggetti inanimati randomicamente tra la seconda e la penultima colonna
        if len(Main.inanimated_in_game)<=5:
            for inanimatedd in Main.inanimate_objects_inventory:
                random_count=0
                while random_count <= random.randint(1,3):
                    #creo l oggetto inanimato
                    new_inanimated=Inanimated(inanimatedd.nome)
                    new_inanimated.img=Main.inanimate_objects_images[random.randrange(0,len(Main.inanimate_objects_images))]
                    Main.inanimated_in_game.append(new_inanimated)

                    #scelgo la cella per l oggetto inanimato
                    viablecells=[]
                    for cell in Main.hex_cells:
                        if cell.col not in range(Main.COL_COUNT-2,Main.COL_COUNT) and cell.col not in range(0,2) and cell.occupied==False:  
                            
                            viablecells.append(cell)
                    randomcell=viablecells[random.randrange(0,len(viablecells)-1)]
                    new_inanimated.x=randomcell.center[0]
                    new_inanimated.y=randomcell.center[1]
                    new_inanimated.getCenter(new_inanimated.x,new_inanimated.y)
                    random_count+=1
                    new_inanimated.createMask()
                    new_inanimated.getParentCell()
            
            print(Main.inanimated_in_game)
                    
        
    def moveCamera(self):

        starting_resizable_layer_x=Main.resizable_layer_x
        starting_resizable_layer_y=Main.resizable_layer_y

        if pygame.mouse.get_pressed()[1]:
            starting_mouse_x = pygame.mouse.get_pos()[0]
            starting_mouse_y = pygame.mouse.get_pos()[1]
            for event in pygame.event.get():

                if event.type == pygame.MOUSEMOTION:
                    
                    """ Main.resizable_layer_x+=pygame.mouse.get_pos()[0]-starting_mouse_x
                    Main.resizable_layer_y+=pygame.mouse.get_pos()[1]-starting_mouse_y """
                    
                    #devo muovere anche tutte le x e y di tutte le unita
                    for player in Main.players:
                        for unit in player.units:
                            unit.x+=pygame.mouse.get_pos()[0]-starting_mouse_x
                            unit.y+=pygame.mouse.get_pos()[1]-starting_mouse_y
                            if unit.middle!=None:
                                unit.middle[0]+=pygame.mouse.get_pos()[0]-starting_mouse_x
                                unit.middle[1]+=pygame.mouse.get_pos()[1]-starting_mouse_y
                                unit.start_x+=pygame.mouse.get_pos()[0]-starting_mouse_x
                                unit.start_y+=pygame.mouse.get_pos()[1]-starting_mouse_y
                            unit.getCenter(unit.x,unit.y)
                            unit.createMask()
                            unit.getParentCell()

                    for cell in Main.hex_cells:
                        cell.center[0]+=pygame.mouse.get_pos()[0]-starting_mouse_x
                        cell.center[1]+=pygame.mouse.get_pos()[1]-starting_mouse_y
                        cell.vertices=[]
                        cell.vertices_create()
                        cell.create_rect_mask()
                    
                    for inan in Main.inanimated_in_game:
                        inan.x+=pygame.mouse.get_pos()[0]-starting_mouse_x
                        inan.y+=pygame.mouse.get_pos()[1]-starting_mouse_y
                        inan.getCenter(inan.x,inan.y)
                        inan.createMask()
                        inan.getParentCell()
                
                else:
                    Main.resizable_layer_x=starting_resizable_layer_x
                    Main.resizable_layer_y=starting_resizable_layer_y
                    
    def gridAndUnitsZoom(self):

        zoomey=0
        if Main.zoom <2:
            Main.speed=20
            Main.zoom=2
            zoomey=2
        else:
            Main.speed=10
            Main.zoom=1  #THIS IS FOR DTS
            zoomey=0.5   #THIS IS FOR CHANGING IMAGES SIZE
        

        
        Main.cell_layer=pygame.transform.scale(Main.cell_layer,(Main.cell_layer.get_width()*zoomey,Main.cell_layer.get_height()*zoomey))
        Main.cell_layer2=pygame.transform.scale(Main.cell_layer2,(Main.cell_layer2.get_width()*zoomey,Main.cell_layer2.get_height()*zoomey))
        Main.unit_layer=pygame.transform.scale(Main.unit_layer,(Main.unit_layer.get_width()*zoomey,Main.unit_layer.get_height()*zoomey))
        for player in Main.players:
            for unit in player.units:
                
                unit.col=unit.parentcell.col
                unit.row=unit.parentcell.row

        for inan in Main.inanimated_in_game:
            inan.col=inan.parentcell.col
            inan.row=inan.parentcell.row
        
        Main.HEX_RADIUS*=zoomey
        Main.hex_cells=[]
        Main.create_grid()

        for player in Main.players:
            for unit in player.units:
                

                if unit.animation[0]!=None:
                    for i in range(len(unit.animation[0][0])):
                        unit.animation[0][0][i]=pygame.transform.scale(unit.animation[0][0][i],(unit.animation[0][0][i].get_width()*zoomey,unit.animation[0][0][i].get_height()*zoomey))
                if unit.animation[1]!=None:
                    for i in range(len(unit.animation[1][0])):
                        unit.animation[1][0][i]=pygame.transform.scale(unit.animation[1][0][i],(unit.animation[1][0][i].get_width()*zoomey,unit.animation[1][0][i].get_height()*zoomey))
                if unit.animation[2]!=None:
                    for i in range(len(unit.animation[2][0])):
                        unit.animation[2][0][i]=pygame.transform.scale(unit.animation[2][0][i],(unit.animation[2][0][i].get_width()*zoomey,unit.animation[2][0][i].get_height()*zoomey))
                if unit.animation[3]!=None:
                    for i in range(len(unit.animation[3][0])):
                        unit.animation[3][0][i]=pygame.transform.scale(unit.animation[3][0][i],(unit.animation[3][0][i].get_width()*zoomey,unit.animation[3][0][i].get_height()*zoomey))
                    
                if unit.img[0] != None:
                    unit.img[0]=pygame.transform.scale(unit.img[0],(unit.img[0].get_width()*zoomey,unit.img[0].get_height()*zoomey))

                if unit.img[1] != None:
                    unit.img[1]=pygame.transform.scale(unit.img[1],(unit.img[1].get_width()*zoomey,unit.img[1].get_height()*zoomey))

                if unit.img[2] != None:
                    unit.img[2]=pygame.transform.scale(unit.img[2],(unit.img[2].get_width()*zoomey,unit.img[2].get_height()*zoomey))

                if unit.img[3] != None:
                    unit.img[3]=pygame.transform.scale(unit.img[3],(unit.img[3].get_width()*zoomey,unit.img[3].get_height()*zoomey))

                if unit.orig_img[0] != None:
                    unit.orig_img[0]=pygame.transform.scale(unit.orig_img[0],(unit.orig_img[0].get_width()*zoomey,unit.orig_img[0].get_height()*zoomey))
                
                if unit.orig_img[1] != None:
                    unit.orig_img[1]=pygame.transform.scale(unit.orig_img[1],(unit.orig_img[1].get_width()*zoomey,unit.orig_img[1].get_height()*zoomey))
                
                if unit.orig_img[2] != None:
                    unit.orig_img[2]=pygame.transform.scale(unit.orig_img[2],(unit.orig_img[2].get_width()*zoomey,unit.orig_img[2].get_height()*zoomey))
                
                if unit.orig_img[3] != None:
                    unit.orig_img[3]=pygame.transform.scale(unit.orig_img[3],(unit.orig_img[3].get_width()*zoomey,unit.orig_img[3].get_height()*zoomey))

                
                for cell in Main.hex_cells:
                    if cell.col==unit.col and cell.row==unit.row:
                        unit.x=cell.center[0]
                        unit.y=cell.center[1]
                        unit.getCenter(unit.x,unit.y)
                        unit.createMask()
                        unit.getParentCell()
                        cell.occupied=True

        for inan in Main.inanimated_in_game:
            if inan.img!=None:
                inan.img=pygame.transform.scale(inan.img,(inan.img.get_width()*zoomey,inan.img.get_height()*zoomey))
            for cell in Main.hex_cells:
                if cell.col==inan.col and cell.row==inan.row:
                    inan.x=cell.center[0]
                    inan.y=cell.center[1]
                    inan.getCenter(inan.x, inan.y)
                    inan.createMask()
                    inan.getParentCell()
                    cell.occupied=True
                
                
            
        



       
        
