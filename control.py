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
        if self.overlayedUnit!=None:
            x=10
            y=Main.screen.get_height()-self.overlayedUnit_overlay.get_height()
            inventory=pygame.image.load("media/ObjectInfo_inventory.png")
            
            screen.blit(self.overlayedUnit_overlay,(x,y))
            for i in self.overlayedUnit.img:
                if i!=None:
                    
                    screen.blit(i,(x+100,y+95))
                    
            screen.blit(inventory,(x+390,y+40))

            
            if self.overlayedUnit.img[2]!=None:
                screen.blit(self.overlayedUnit.img[2], (x+390+80, y+70))

            
            if self.overlayedUnit.img[0]!=None:
                screen.blit(self.overlayedUnit.img[0], (x+390+80, y+130))

            
            if self.overlayedUnit.img[3]!=None:
                screen.blit(self.overlayedUnit.img[3], (x+390+140 , y+130))

            
            if self.overlayedUnit.img[1]!=None:
                screen.blit(self.overlayedUnit.img[1], (x+390+10, y+130))

            hp=Main.font.render('Hp:', True, (29,12,28))
            hp=pygame.transform.scale(hp, (hp.get_width()/2, hp.get_height()/2))
            screen.blit(hp, (x+60, y+164))

            atk=Main.font.render('Attack:'+str(self.overlayedUnit.atk), True, (29,12,28))
            atk=pygame.transform.scale(atk, (atk.get_width()/2, atk.get_height()/2))
            screen.blit(atk, (x+220, y+164))

            name=Main.font.render('Name:'+str(self.overlayedUnit.nome), True, (29,12,28))
            name=pygame.transform.scale(name, (name.get_width()/2, name.get_height()/2))
            screen.blit(name, (x+220, y+100))

            self.overlayedUnit.drawHpBar(screen,80,15,x+90+Main.resizable_layer_x,y+160+Main.resizable_layer_y)

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

                if event.type == pygame.MOUSEMOTION and Main.controller.gameFase==1:
                    
                    Main.resizable_layer_x+=pygame.mouse.get_pos()[0]-starting_mouse_x
                    Main.resizable_layer_y+=pygame.mouse.get_pos()[1]-starting_mouse_y
                    
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
                    

                    

            
    """ def AdaptObjectsToScreenSize(self,resize_x,resize_y):
        
        for player in Main.players:
                for unit in player.units:
                    unit.x+=resize_x
                    unit.y+=resize_y
                    if unit.middle!=None:
                        unit.middle[0]+=resize_x
                        unit.middle[1]+=resize_y
                        unit.start_x+=resize_x
                        unit.start_y+=resize_y
                    unit.getCenter(unit.x,unit.y)
                    unit.createMask()
                    unit.getParentCell()

        for cell in Main.hex_cells:
            cell.center[0]+=resize_x
            cell.center[1]+=resize_y
            
            cell.create_rect_mask()
        
        for inan in Main.inanimated_in_game:
            inan.x+=resize_x
            inan.y+=resize_y
            inan.getCenter(inan.x,inan.y)
            inan.createMask()
            inan.getParentCell()

        for men in Main.menus :
            men.x+=resize_x
            men.y+=resize_y

            

            for butto in men.buttons:
                butto.x+=resize_x
                butto.y+=resize_y """
                

                #print(butto.x,butto.y)

                
            
        



       
        
