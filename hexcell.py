import pygame
import math
import Main
import random
from polygon import Polygono
from shapely.geometry import Polygon, Point, LineString
import copy
from line import Line


# classe oggetto cella
# ----------------------------------------------------------------------------------------------------------------------------------------------------
class HexCell:
    def __init__(self, row, col, center, radius, img):
        self.row = row
        self.col = col
        self.center = center
        self.radius = radius
        self.selected = False
        self.vertices = []
        self.vertices_create()
        self.rectMask = []
        self.maskForBarrier = None

        self.create_rect_mask()
        self.dts = 999  # DISTANCE TO SELECTED
        self.occupied = False
        self.img = pygame.transform.scale(img, (self.radius * 2, self.radius * 2))
        self.blockedForMovement = False

    # trovo e creo i vertici dell'esagono
    def vertices_create(self):
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(
                angle_deg
            )  # trasformo i gradi angolari in radianti per farci il seno/coseno sotto
            x = self.center[0] + self.radius * math.cos(angle_rad)
            y = self.center[1] + self.radius * math.sin(angle_rad)
            self.vertices.append([x, y])

    # disegno l'esagono
    def draw(self, screen):
        # randomcell=random.randint(0,1)
        screen.blit(
            self.img,
            (
                self.center[0] - self.img.get_width() / 2,
                math.ceil(self.center[1] - self.img.get_height() / 2),
            ),
        )
        if Main.controller.actingUnit == None and Main.controller.actingPlayer == 0:
            self.illuminateCell(Main.cell_layer2)
            self.illuminateCellAtk(Main.cell_layer2)
        """ #tests
        if self.blockedForMovement==True:
            pygame.draw.polygon(screen, (191, 117, 75), self.vertices, 0)
            pygame.draw.polygon(screen, (34, 32, 52), self.vertices, 2) 
        if self.occupied==True:
            pygame.draw.polygon(screen, (255, 117, 75), self.vertices, 0)
            pygame.draw.polygon(screen, (34, 255, 52), self.vertices, 2) """
        """ for i in self.masksForBarrier:
            pygame.draw.rect(Main.cell_layer2, (2, 255, 78), i[0], 0) """
        """ for i in self.rectMask:
            pygame.draw.rect(Main.cell_layer2, (2, 255, 78), i, 0)
        pygame.draw.rect(Main.cell_layer2, (2, 25, 78), pygame.Rect((self.center[0] - 5, self.center[1] - 5), (10, 10)), 0) """

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
        self.maskForBarrier=Polygon(
            [
                (self.center[0] - 5, self.center[1] - 5),
                (self.center[0] - 5 + 10, self.center[1] - 5),
                (self.center[0] - 5 + 10, self.center[1] - 5 + 10),
                (self.center[0] - 5, self.center[1] - 5 + 10),
            ]
        )
        

    # funzione per checkare le collisioni del mouse con il brutto rectMask
    def checkHexMousecollision(self):
        mouse_pos = pygame.mouse.get_pos()
        return self if any(rect.collidepoint(mouse_pos[0], mouse_pos[1]) for rect in self.rectMask) else None

    # funzione distanza dal selezionato 1

    def dtsf(self):  # dtsf=DISTANCE TO SELECTED FUNCTION
        for x in range(Main.maximum(Main.ROW_COUNT, Main.COL_COUNT)):
            if self.dts <= x + 1:
                break
            list_of_measured_cells = []
            for cell in Main.hex_cells:
                if cell.dts == x:
                    list_of_measured_cells.append(cell)
            if len(list_of_measured_cells) == 0:
                return
            else:
                for cell in list_of_measured_cells:
                    if (
                        Main.dist(
                            self.center[0],
                            cell.center[0],
                            self.center[1],
                            cell.center[1],
                        )
                        <= 100 * Main.zoom
                        and self.dts >= x + 1
                    ):
                        self.dts = x + 1
                        break

    def checkForBarrier(self):
        selected = Main.controller.selectedd
        self.blockedForMovement = False
        potential_barriers =[
            cell
            for cell in Main.hex_cells
            if cell.occupied == True
            and cell != self
            and cell !=selected.parentcell
            and cell.dts <= self.dts
            and cell.dts <= selected.movepts
        ]

        lines = []
        polygons = []
        bignumber = 1000

        for barrier in potential_barriers:
            barrier_x = barrier.center[0]
            barrier_y = barrier.center[1]
            selected_x = selected.x
            selected_y = selected.y
            dist_selected_barrier = Main.dist(selected_x, barrier_x, selected_y, barrier_y)
            line_x = barrier_x + (bignumber * (barrier_x - selected_x)) / dist_selected_barrier
            line_y = barrier_y + (bignumber * (barrier_y - selected_y)) / dist_selected_barrier
            lines.append([LineString([(selected_x, selected_y), (line_x, line_y)]), barrier])

            for barrier1 in potential_barriers:
                if barrier != barrier1:
                    dist_barrier_barrier1 = Main.dist(barrier_x, barrier1.center[0], barrier_y, barrier1.center[1])
                    if dist_barrier_barrier1 <= 110 * Main.zoom:
                        for line in lines:
                            for line1 in lines:
                                if line[1] == barrier and line1[1] == barrier1:
                                    barrier1_x = barrier1.center[0]
                                    barrier1_y = barrier1.center[1]
                                    line1_x = barrier1_x + (bignumber * (barrier1_x - selected_x)) / Main.dist(selected_x, barrier1_x, selected_y, barrier1_y)
                                    line1_y = barrier1_y + (bignumber * (barrier1_y - selected_y)) / Main.dist(selected_x, barrier1_x, selected_y, barrier1_y)
                                    polygons.append([Polygon([(selected_x, selected_y), (line_x, line_y), (line1_x, line1_y)]), barrier, barrier1])

        for line in lines:
            #pygame.draw.line(Main.layout_layer, (255, 0, 0), (selected.x,selected.y), (line[1].center[0], line[1].center[1]), 1)
            if line[0].intersects(self.maskForBarrier):
                self.blockedForMovement = True

        for polygon in polygons:
            #pygame.draw.polygon(Main.layout_layer, (255, 0, 0,30), polygon[0].exterior.coords, 0)
            if polygon[0].intersects(self.maskForBarrier) and self.dts > polygon[1].dts:
                self.blockedForMovement = True

    # illumino la cella se in range col selected
    def illuminateCell(self, screen):
        if (
            Main.controller.selectedd != None
            and self.dts <= Main.controller.selectedd.movepts
            and self.occupied == False
            and Main.controller.selectedd.movepts > 0
            and self.blockedForMovement == False
        ):
            pygame.draw.polygon(screen, (255, 255, 0, 40), self.vertices)

    # illumino la cella se in atkrange
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
