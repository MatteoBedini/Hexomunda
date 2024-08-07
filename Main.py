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
from layout import Layout
import data


# Inizializza Pygame
pygame.init()




clock = pygame.time.Clock()
elapsed_time = 0


# costanti varie
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('data/fonts/Press_Start_2P/PressStart2P-Regular.ttf', 64)
font1 = pygame.font.Font('freesansbold.ttf', 64)
#font1 = pygame.font.Font('data/fonts/yoster-island/yoster.ttf', 128)
#font1 = pygame.font.Font('data/fonts/pricedown/pricedown bl.otf', 128)
#font1 = pygame.font.Font('data/fonts/game-over/GameOver/game over.ttf', 32)

screen_info = pygame.display.Info()
# Dimensioni della finestra
width = screen_info.current_w
height = screen_info.current_h

#width=1280
#height=720
layers=[]

screen = pygame.display.set_mode((width, height),pygame.RESIZABLE,pygame.HWSURFACE | pygame.DOUBLEBUF)  # z-index=0 #sopra non ci va niente,solo lo sfondo
cell_layer = pygame.Surface((width, height), pygame.SRCALPHA)  # z-index=1
cell_layer2=pygame.Surface((width, height), pygame.SRCALPHA)  # z-index=2
unit_layer = pygame.Surface((width, height), pygame.SRCALPHA)  # z-index=3
overlays_layer = pygame.Surface((width, height), pygame.SRCALPHA)  # z-index=4
menu_box_layer = pygame.Surface((width, height), pygame.SRCALPHA)  #z-index=5
menu_buttons_layer = pygame.Surface((width, height), pygame.SRCALPHA)  #z-index=6
""" overlay_menu_box_layer = pygame.Surface((width, height), pygame.SRCALPHA)  #z-index=7
overlay_menu_buttons_layer = pygame.Surface((width, height), pygame.SRCALPHA)  #z-index=8 """
layout_layer = pygame.Surface((width, height), pygame.SRCALPHA)  #z-index=9

general_changed=False
screen_changed=False
cell_layer_changed=False
cell_layer2_changed=False
unit_layer_changed=False
overlays_layer_changed=False
menu_box_layer_changed=False
menu_buttons_layer_changed=False
overlay_menu_box_layer_changed=False
overlay_menu_buttons_layer_changed=False
layout_layer_changed=False

vw=screen.get_width()
vh=screen.get_height()


zoom=1


resizable_layer_x=0
resizable_layer_y=0

layers.append(cell_layer)
layers.append(cell_layer2)
layers.append(unit_layer)
layers.append(menu_box_layer)
layers.append(menu_buttons_layer)
""" layers.append(overlay_menu_box_layer)
layers.append(overlay_menu_buttons_layer) """
layers.append(overlays_layer)
layers.append(layout_layer)





pygame.display.set_caption("Warbands")

# costanti per la griglia esagonale
HEX_RADIUS = 50  # Raggio dell'esagono
ROW_COUNT = random.randrange(7,9)   # Numero di righe
COL_COUNT = random.randrange(13,15)   # Numero di colonne
APOTEMA= math.floor(math.sqrt(3) * HEX_RADIUS)/2


""" grid_xx = (width - COL_COUNT * 1.5 * HEX_RADIUS) / 2
grid_yy = (height - ROW_COUNT * math.floor(math.sqrt(3) * HEX_RADIUS)) / 2 """
""" grid_surface_width = COL_COUNT * 1.5 * HEX_RADIUS #+ grid_xx * 2
grid_surface_height = ROW_COUNT * math.floor(math.sqrt(3) * HEX_RADIUS) #+ grid_yy * 2
cell_layer=pygame.transform.scale(cell_layer, (grid_surface_width, grid_surface_height))
cell_layer2=pygame.transform.scale(cell_layer2, (grid_surface_width, grid_surface_height))
unit_layer=pygame.transform.scale(unit_layer, (grid_surface_width, grid_surface_height)) """

# Calcola le dimensioni totali della griglia esagonale
grid_width = 1.5 * HEX_RADIUS * COL_COUNT
grid_height = (math.sqrt(3) * HEX_RADIUS) * ROW_COUNT
grid_x = width/5 #(width - grid_width) / 2  # Calcola la posizione X per centrare la griglia
grid_y = height/5  # Calcola la posizione Y per centrare la griglia

#variabili varie
speed=10



# funzioni generali
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# funzione calcola distanza tra due punti
def dist(x1, x2, y1, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

#massimo fra 2 numeri
def maximum(a, b):
    if a >= b:
        return a
    else:
        return b
    
def getLinePoints(punto1, punto2):
        punti = []
        distanza_x = punto2[0] - punto1[0]
        distanza_y = punto2[1] - punto1[1]
        distanza_totale = int(max(abs(distanza_x), abs(distanza_y)))

        for i in range(distanza_totale + 1):
            x = punto1[0] + (i / distanza_totale) * distanza_x
            y = punto1[1] + (i / distanza_totale) * distanza_y
            punti.append((round(x), round(y)))

        return punti



# classe cursor MOUSE
# -----------------------------------------------------------------------------------------------------------------------------------------------------
class cursorr:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("./media/cursor1.png")

    def drawcursor(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, x, y):
        self.x = x
        self.y = y
        self.drawcursor()


cursor = cursorr(250, 250)



# creazione oggetti
# -------------------------------------------------------------------------------------------------------------------------------------------------
# creo il control
controller = Control()

#immagini celle
cells_img = [pygame.image.load("./media/cell1.png"), pygame.image.load("./media/cell2.png")] #, pygame.image.load("./media/cell3.png")
# creo la griglia
hex_cells = []
def create_grid():
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):

            x = (
                col * 1.5 * HEX_RADIUS + grid_x
            )  # Aggiungo l'offset per centrare nello schermo

            y = (
                row * math.floor(math.sqrt(3)* HEX_RADIUS) + grid_y
            )  # Aggiungo l'offset per centrare nello schermo
            if col % 2 == 1:
                y += math.floor(math.sqrt(3) / 2 * HEX_RADIUS)

            center = [x, y]
            hex_cells.append(HexCell(row, col, center, HEX_RADIUS,cells_img[random.randint(0,len(cells_img)-1)]))

create_grid()


# creo le unità
deadunits = []
players = []
players.append(Player(9999,False))
players.append(Player(25,True))
players[0].units=[]
players[1].units= []



units_type_INVENTORY = []   #tipi di unità predefiniti da mettere nel menu di scelta e creazione unità del giocatore
units_type_INVENTORY.append(
    Unit(

        False,
        1,
        'orc',
        'orc'
    )
)
units_type_INVENTORY.append(
    Unit(

        False,
        1,
        'goblin',
        'goblin'
    )
)
units_type_INVENTORY.append(
    Unit(

        False,
        1,
        'human',
        'human'
    )
)
units_type_INVENTORY.append(
    Unit(

        False,
        1,
        'dwarf',
        'dwarf'
    )
)

all_races=[[],[],[],[]] #array per il menu di selezione unità, un array per ogni razza per i pulsanti



#creo i menu e pulsanti vari
menus=[]                                    #lista di tutti i menu

mainMenu=Menu(screen.get_width()/4,screen.get_height()/2,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'mainmenu')                       #menu principale

load_game_menu=Menu(screen.get_width()/4,screen.get_height()/2,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'load game') #menu di caricamento
unitsInventoryMenu=Menu(screen.get_width()/3,screen.get_height()/2,screen.get_width()/2-screen.get_width()/4,screen.get_height()/4,'unitsInventoryMenu')   #menu per l'inventario di unità

menu1=Menu(screen.get_width()-300,130,150,0+height-140,'upi')                                     #menu for unit placing in grid

end_turn_button=Button(screen.get_width()-150,screen.get_height()-100,80,40,'endTurn','end',None)

skirmish_menu=Menu(screen.get_width()/4,screen.get_height()/2,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'skirmish')                       #menu preparazione skirmish

options_menu=Menu(screen.get_width()-600,450,300,0+height-700,'options')                       #menu opzioni

pause_menu=Menu(screen.get_width()/4,screen.get_height()/2,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'pausemenu')

victory_view=Menu(screen.get_width()/4,screen.get_height()/3,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'victory')
defeat_view=Menu(screen.get_width()/4,screen.get_height()/3,screen.get_width()/2-screen.get_width()/8,screen.get_height()/4,'defeat')

shop_overlay_active=False
shop_overlay_menu=Menu(screen.get_width()/3,screen.get_height()/100*70,unitsInventoryMenu.x+unitsInventoryMenu.width,unitsInventoryMenu.y-(screen.get_height()/100*70-unitsInventoryMenu.height)/2,'shop_overlay')
#shop_overlay_buttons=[]
#shop_overlay_rect=pygame.Rect(300,300,screen.get_width()/2,screen.get_height()/2)

menus.append(mainMenu)
menus.append(unitsInventoryMenu)
menus.append(menu1)
#menus.append(end_turn_button)
menus.append(skirmish_menu)
menus.append(options_menu)
menus.append(pause_menu)


#others
scrollbars=[]
# definizione dell'appartenenza al giocatore delle unit
for player in players:
    for unit in player.units:
        unit.definePlayer()

#creo la room/level
room=Room()

#oggetti inanimati:
inanimate_objects_images=[pygame.image.load('./media/tree1.png'),pygame.image.load('./media/tree2.png')]
inanimate_objects_inventory=[]
inanimate_objects_inventory.append(Inanimated('tree1'))

inanimated_in_game=[]

#layout
layout=Layout()

""" def reset_after_changes():
    if general_changed:
        if cell_layer_changed:
            cell_layer.fill((0, 0, 0, 0))
def blit_after_screen_changes():
    if general_changed:
        if cell_layer_changed:
            screen.blit(cell_layer,(resizable_layer_x,resizable_layer_y))
        if cell_layer2_changed:
            screen.blit(cell_layer2,(resizable_layer_x,resizable_layer_y))
        if unit_layer_changed:
            screen.blit(unit_layer,(resizable_layer_x,resizable_layer_y))
        if menu_box_layer_changed:
            screen.blit(menu_box_layer,(0,0))
        if menu_buttons_layer_changed:
            screen.blit(menu_buttons_layer,(0,0))
        if overlays_layer_changed:
            screen.blit(overlays_layer,(0,0))

 """

# Ciclo di gioco
# ----------------------------------------------------------------------------------------------------------------------------------------------------
running = True
while running:
    DELTA=1/pygame.time.get_ticks()
    # Calcola il tempo trascorso
    elapsed_time += clock.get_rawtime()
    


    screen.fill((16, 26, 38))
    #cell_layer.fill((0, 0, 0, 0))  # pulisco gli schermi, i layers li faccio trasparenti
    cell_layer2.fill((0, 0, 0, 0))  
    unit_layer.fill((0, 0, 0, 0))  
    menu_box_layer.fill((0, 0, 0, 0))  
    menu_buttons_layer.fill((0, 0, 0, 0))  


    match room.roomNumber:
        case 0:
            #MAIN MENU
            mainMenu.draw(menu_box_layer)
            for butto in mainMenu.buttons:
                butto.input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        #case 4:
            #OPTIONS MENU


            #options_menu.draw(menu_box_layer)
            #for button in options_menu.buttons:
                #button.input()

            #for event in pygame.event.get():

                #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                   # room.roomNumber=0


                #if event.type == pygame.QUIT:
                    #running = False
        case 3:
            #SKIRMISH preparazione
            skirmish_menu.draw(menu_box_layer)
            for button in skirmish_menu.buttons:
                button.input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                    room.roomNumber=0

        case 1:
            #menu scelta unità e occupazione inventario unità

            unitsInventoryMenu.draw(menu_box_layer)

            if shop_overlay_active==False:
                for butto in unitsInventoryMenu.buttons:
                    butto.input()


            for unit in players[0].units_inventory:
               unit.draw(menu_buttons_layer)

            if shop_overlay_active==True:


                #draw rettangolone dell'overlay


                shop_overlay_menu.draw(menu_box_layer)
                for button in shop_overlay_menu.buttons:
                    button.draw(menu_buttons_layer)
                    button.input()
                    button.otherEvents()
                
                for scrollbar in scrollbars:
                    scrollbar.draw(menu_buttons_layer)
                    scrollbar.scroller.input()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                    room.roomNumber=0

        case 2:
            #muovi camera
            controller.moveCamera()

            #HEXGRID GAME
            overlays_layer.fill((0, 0, 0, 0))
            #fase 1 piazzamento unita
            if controller.gameFase==0:
                controller.checkOccupiedCells()
                for player in players:
                    player.ai_units_random_choice()
                    if player.ai==True and player.ai_selection_ended==True:
                            controller.ai_pos()

                menu1.draw(menu_box_layer)
                for butto in menu1.buttons:
                    butto.input()
                    butto.moveFakeBoy()
                for unit in players[0].units:
                    unit.draw(unit_layer)


                controller.InanimatePlace()
                for objectt in inanimated_in_game:
                    objectt.draw(unit_layer)


            #disegno le celle fuori dalle game fases
            for cell in hex_cells:
                cell.draw(screen)
                cell.checkHexMousecollision()


            #fase 2 gioco
            if controller.gameFase==1:


                controller.unitStart()
                if controller.actingUnit==None:
                    controller.checkOccupiedCells()
                    controller.ai_select_control()
                controller.drawObjectOverlay(menu_buttons_layer)


                for objectt in inanimated_in_game:
                    objectt.draw(unit_layer)


                if controller.actingPlayer==0 and controller.actingUnit==None:
                    end_turn_button.draw(menu_buttons_layer)
                    end_turn_button.input()


                for player in players:
                    if player.ai==True and controller.actingUnit==None:
                        player.ai_turn_end_control()   #se tutte le unit sono aifinishedturn=true allora turnend()
                        for unit in player.units:
                            if unit.activated==True:
                                unit.aiEndTurn()
                                unit.resectSelect()
                                unit.attack()
                                unit.select()
                                unit.move()
                                unit.getParentCell()

                for player in players:

                    for unit in player.units:

                        unit.moveAnimation()
                        unit.attackOfOpportunity()
                        unit.attackAnimation(5*zoom)
                        unit.draw(unit_layer)
                
                controller.drawAnimations()


            #fuori dalle fasi ma dentro la room 2
            for event in pygame.event.get():


                if event.type == pygame.QUIT:       #esci dal gioco
                        running = False

                if controller.actingUnit==None:



                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                        room.roomNumber=5

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        if controller.gameFase==1:
                            controller.gridAndUnitsZoom()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if controller.gameFase==1:
                            data.save()

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if controller.gameFase==1:
                            
                            for player in players:
                                for unit in player.units:
                                    controller.createObjectOverlay(unit)
                                    if unit.activated==True:
                                        unit.aiEndTurn()  # unit-->aifinishedturn=true
                                        unit.resectSelect()
                                        unit.attack()
                                        unit.select()
                                        unit.move()

        #pause menu
        case 5:
           
            pause_menu.draw(menu_box_layer)
            for butto in pause_menu.buttons:
                butto.input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                        room.roomNumber=2

        #end game screen
        case 6:
            controller.matchResultControl()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                        room.roomNumber=0
        
        #load games view
        case 7:
            load_game_menu.draw(menu_box_layer)
            for butto in load_game_menu.buttons:
                butto.input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #torna al main menu
                        room.roomNumber=0


    layout.draw()
    
    """ cursor.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) """

    #ridisegno gli schermi
    #screen.blit(cell_layer,(resizable_layer_x,resizable_layer_y))
    screen.blit(cell_layer2,(resizable_layer_x,resizable_layer_y))
    screen.blit(unit_layer,(resizable_layer_x,resizable_layer_y))
    screen.blit(menu_box_layer,(0,0))
    screen.blit(menu_buttons_layer,(0,0))
    
    clock.tick(144)
    fpss = clock.get_fps()

    # Print FPS to console
    """ print(f"FPS: {fpss}") """

    pygame.display.update()
    


# Chiudi Pygame quando esci dal ciclo di gioco
pygame.quit()






