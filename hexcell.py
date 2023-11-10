import pygame
import math
import Main
import random



# classe oggetto cella
# ----------------------------------------------------------------------------------------------------------------------------------------------------
class HexCell:
    def __init__(self, row, col, center, radius,img):
        self.row = row
        self.col = col
        self.center = center
        self.radius = radius
        self.selected = False
        self.vertices = []
        self.vertices_create()
        self.rectMask = []
        self.create_rect_mask()
        self.dts = 999  # DISTANCE TO SELECTED
        self.occupied = False
        self.img=img

    # trovo e creo i vertici dell'esagono
    def vertices_create(self):
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(
                angle_deg
            )  # trasformo i gradi angolari in radianti per farci il seno/coseno sotto
            x = self.center[0] + self.radius * math.cos(angle_rad)-Main.resizable_layer_x
            y = self.center[1] + self.radius * math.sin(angle_rad)-Main.resizable_layer_y
            self.vertices.append([x, y])

    # disegno l'esagono
    def draw(self, screen):
        """ pygame.draw.polygon(screen, (191, 117, 75), self.vertices, 0)
        pygame.draw.polygon(screen, (34, 32, 52), self.vertices, 2) """
        #randomcell=random.randint(0,1)
        screen.blit(self.img, (self.center[0]-self.img.get_width()/2-Main.resizable_layer_x, math.ceil(self.center[1]-self.img.get_height()/2-Main.resizable_layer_y)))
        if Main.controller.actingUnit == None and Main.controller.actingPlayer==0:
            self.illuminateCell(Main.cell_layer2)
            self.illuminateCellAtk(Main.cell_layer2)

    # disegno la maschera p er le collisioni fatta male a rettangoli
    def create_rect_mask(self):
        self.rectMask = [
            pygame.Rect((self.center[0] - 30, self.center[1] - 30), (60, 60)),
            pygame.Rect(
                (
                    self.center[0] - (self.vertices[5][0] - self.vertices[4][0]) / 2,
                    self.center[1]
                    - (self.vertices[1][1] - self.vertices[5][1]) / 2
                    + 3,
                ),
                (
                    (self.vertices[5][0] - self.vertices[4][0] - 1),
                    (self.vertices[1][1] - self.vertices[5][1] - 3),
                ),
            ),
            pygame.Rect((self.center[0] - 40, self.center[1] - 12), (80, 24)),
            pygame.Rect((self.center[0] - 36, self.center[1] - 18), (72, 36)),
            pygame.Rect((self.center[0] - 45, self.center[1] - 6), (90, 12)),
            pygame.Rect((self.center[0] - 33, self.center[1] - 23), (66, 46)),
        ]

    # funzione per checkare le collisioni del mouse con il brutto rectMask
    def checkHexMousecollision(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rectMask[0].collidepoint(mouse_pos[0], mouse_pos[1])
            or self.rectMask[1].collidepoint(mouse_pos[0], mouse_pos[1])
            or self.rectMask[2].collidepoint(mouse_pos[0], mouse_pos[1])
            or self.rectMask[3].collidepoint(mouse_pos[0], mouse_pos[1])
            or self.rectMask[4].collidepoint(mouse_pos[0], mouse_pos[1])
            or self.rectMask[5].collidepoint(mouse_pos[0], mouse_pos[1])
        ):
            #pygame.draw.polygon(Main.layer2, (255, 115, 115), self.vertices, 2)
            return self
        else:
            return None

    # funzione distanza dal selezionato 1

    def dtsf(self):  # dtsf=DISTANCE TO SELECTED FUNCTION
        for x in range(Main.maximum(Main.ROW_COUNT, Main.COL_COUNT)):
            if self.dts <= x + 1:
                break
            list_of_measured_cells = []
            for cell in Main.hex_cells:
                
                if (
                    cell.dts == x
                    
                ):
                    list_of_measured_cells.append(cell)
            if len(list_of_measured_cells)==0:
                return
            else:
                for cell in list_of_measured_cells:
                    if(
                        Main.dist(self.center[0], cell.center[0], self.center[1], cell.center[1])<= 100
                        and self.dts >=x + 1
                    ):
                        self.dts = x + 1
                        break
                
            
                
        

    

    # illumino la cella se in range col selected
    def illuminateCell(self, screen):
        if (
            Main.controller.selectedd != None
            and self.dts <= Main.controller.selectedd.movepts
            and self.occupied==False
            # and hexagon.controller.selectedd.movepts>0
        ):
            pygame.draw.polygon(screen, (255, 255, 0, 40), self.vertices)

    #illumino la cella se in atkrange
    def illuminateCellAtk(self, screen):
        if (
            Main.controller.selectedd != None
            and self.dts <= Main.controller.selectedd.atkrange
            and Main.controller.selectedd.atkpts > 0
        ):
            
            for player in Main.players:
                for unit in player.units:
                    if unit.activated == False and unit.parentcell == self:
                        pygame.draw.polygon(screen, (255, 0, 0, 125), self.vertices, 9)




            
            