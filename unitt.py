import pygame
import Main
import equipment
import hexcell


# classe unità
# -------------------------------------------------------------------------------------------------------------------------------------------------
class Unit:
    def __init__(self, ai, id, nome, race):
        # nome e id
        self.id = id
        self.nome = nome

        # posizione
        self.x = 0
        self.y = 0
        self.col=0
        self.row=0

        # immagine e centro immagine
        self.center = [0, 0]
        self.img = [None, None, None, None]

        self.orig_img = [None, None, None, None]  # template [body,rhand,head,lhand]

        self.flipChecker = False
        # self.getCenter(self.x, self.y)

        # statistiche di gioco
        self.hp = 1
        self.maxhp = 1

        self.totmovepts = 1
        self.movepts = 1

        self.atk = 1
        self.atkpts = 1
        self.totatkpts = self.atkpts
        self.atkrange = 1

        # maschera
        self.rectMask = []
        self.mask = [None, None, None, None]
        self.glow = [None, None, None, None]

        # hexcell di locazione
        self.rectForParent = None  # rettangolino per centrare l'unita nell'esagono
        self.parentcell = None
        self.getParentCell()

        self.player = None

        # ai
        self.ai = ai
        self.aiFinishedTurn = False

        # movemento
        self.activated = False
        self.selected = False
        self.move_target = None
        self.moving = False
        self.moved = False

        # animazione d'attacco
        self.attacked_target = None
        self.middle = [0, 0]
        self.start_x = 0
        self.start_y = 0
        self.attacked_target_returning = False

        # modifiers
        self.race = race
        self.applyRaceModifiers()
        self.basestats = [
            self.maxhp,
            self.atk,
            self.totatkpts,
            self.totmovepts,
            self.atkrange,
        ]
        self.inventory = {
            "head": "",
            "body": "",
            "lhand": "",
            "rhand": "",
        }
        self.applyEquipmentModifiers()

    # assegno l'unit a un giocatore
    def definePlayer(self):
        self.player = next(
            i for i, playerunits in enumerate(Main.players) if self in playerunits.units
        )

    # per spostare l'immagine al centro invece che in basso a destra
    def getCenter(self, x, y):
        self.center[0] = x - ((self.img[1].get_width()) / 2)
        self.center[1] = y - ((self.img[1].get_height()) / 2)

    # disegno
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        # illumino l'omino in base alla maschera se ci passo sopra col mouse
        if self.rectMask.collidepoint(mouse_pos[0], mouse_pos[1]) == True:
            for i in self.glow:
                if i != None:
                    for dot in i:
                        pygame.draw.rect(
                            screen,
                            (247, 247, 247),
                            pygame.Rect(
                                dot[0] + self.center[0] - Main.resizable_layer_x,
                                dot[1] + self.center[1] - Main.resizable_layer_y,
                                1,
                                1,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (247, 247, 247),
                            pygame.Rect(
                                dot[0] + self.center[0] + 1 - Main.resizable_layer_x,
                                dot[1] + self.center[1] - Main.resizable_layer_y,
                                1,
                                1,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (247, 247, 247),
                            pygame.Rect(
                                dot[0] + self.center[0] - 1 - Main.resizable_layer_x,
                                dot[1] + self.center[1] - Main.resizable_layer_y,
                                1,
                                1,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (247, 247, 247),
                            pygame.Rect(
                                dot[0] + self.center[0] - Main.resizable_layer_x,
                                dot[1] + self.center[1] - 1 - Main.resizable_layer_y,
                                1,
                                1,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (247, 247, 247),
                            pygame.Rect(
                                dot[0] + self.center[0] - Main.resizable_layer_x,
                                dot[1] + self.center[1] + 1 - Main.resizable_layer_y,
                                1,
                                1,
                            ),
                        )
        # disegno l'omino
        
        
        for i in self.img:
            
            if i != None:
                
                #i=pygame.transform.scale(i, (i.get_width()*Main.zoom, i.get_height()*Main.zoom))
                screen.blit(
                    i,
                    (
                        self.center[0] - Main.resizable_layer_x,
                        self.center[1] - Main.resizable_layer_y,
                    ),
                )

        # se siamo nella room di gioco degli esagoni faccio vedere la barra della vita
        if Main.room.roomNumber == 2:
            self.drawHpBar(screen, 40, 7, self.center[0] + 12, self.center[1])

    # sottometodo:disegno la barra della vita
    def drawHpBar(self, screen, max, height, x, y):
        hpPercentage = self.hp * 100 / self.maxhp
        rectMaxLength = max
        rectWidth = rectMaxLength * hpPercentage / 100
        if self.ai == True:
            pygame.draw.rect(
                screen,
                (242, 39, 39),
                (
                    x - Main.resizable_layer_x,
                    y + 4 - Main.resizable_layer_y,
                    rectWidth,
                    height,
                ),
                0,
                3,
            )
            pygame.draw.rect(
                screen,
                (34, 32, 52),
                (
                    x - Main.resizable_layer_x,
                    y + 4 - Main.resizable_layer_y,
                    rectMaxLength,
                    height,
                ),
                2,
                3,
            )
        else:
            pygame.draw.rect(
                screen,
                (3, 166, 74),
                (
                    x - Main.resizable_layer_x,
                    y + 4 - Main.resizable_layer_y,
                    rectWidth,
                    height,
                ),
                0,
                3,
            )
            pygame.draw.rect(
                screen,
                (34, 32, 52),
                (
                    x - Main.resizable_layer_x,
                    y + 4 - Main.resizable_layer_y,
                    rectMaxLength,
                    height,
                ),
                2,
                3,
            )
        text = Main.font1.render(
            str(self.hp) + "/" + str(self.maxhp), True, (29, 12, 28)
        )
        text = pygame.transform.scale(text, (rectMaxLength / 2, 10))
        screen.blit(
            text,
            (
                x + rectMaxLength / 4 - Main.resizable_layer_x,
                y - 6 - Main.resizable_layer_y,
            ),
        )

    # memorizzo la cella in cui è posizionata l'unita
    def getParentCell(self):
        self.rectForParent = pygame.Rect((self.x - 5, self.y - 5), (10, 10))

        for cell in Main.hex_cells:
            if self.rectForParent.collidepoint(cell.center[0], cell.center[1]) == True:
                self.parentcell = cell

        if Main.controller.selectedd == self and self.parentcell != None:
            # print("yes parent cell dts is set to zero ")
            self.parentcell.dts = 0

    # creo la maschera per le collisioni
    def createMask(self):
        self.rectMask = pygame.Rect(
            self.center[0],
            self.center[1],
            self.img[1].get_width(),
            self.img[1].get_height(),
        )

        # creo la maschera
        for j in self.img:
            if j != None:
                for i in self.mask:
                    for d in range(4):
                        if self.mask[d] == i and self.img[d] == j:
                            self.mask[d] = pygame.mask.from_surface(j)

        # creo l'outline
        for k in self.mask:
            if k != None:
                for l in self.glow:
                    for d in range(4):
                        if self.glow[d] == l and self.mask[d] == k:
                            self.glow[d] = self.mask[d].outline()

    # resetto il select
    def resectSelect(self):
        # RESET
        if Main.controller.selectedd != self:
            self.selected = False

    # sottometodo:deselezione mini da integrare nella successiva
    def deselect(self):
        Main.controller.selectedd = None
        self.selected = False
        # print("unselected")
        for cell in Main.hex_cells:
            cell.dts = 999

    def recalculateDts(self):
        for cell in Main.hex_cells:
            cell.dtsf() # dtsf=DISTANCE TO SELECTED FUNCTION
        if all(cell.dts != 999 for cell in Main.hex_cells):
            return
        else:
            self.recalculateDts()
        
                

    # seleziono e deseleziono
    def select(self):
        # SELEZIONE PER GIOCATORE
        if (
            self.ai == False
            and self.moving == False
            and Main.controller.actingUnit == None
        ):
            # SELEZIONE
            mouse_pos = pygame.mouse.get_pos()

            if self.rectMask.collidepoint(mouse_pos[0], mouse_pos[1]) == 1:
                if self.selected == False and self.activated == True:
                    for cell in Main.hex_cells:
                        cell.dts = 999
                    self.selected = True
                    # print("selected")
                    Main.controller.selectedd = self
                    self.getParentCell()

                    if self.moved == False:
                        self.recalculateDts()

                    """ if self.moved == False:
                        hexcell.dtsf2(self.parentcell) """

                # DESELEZIONE CLICCANDO SU SE STESSO
                elif self.selected == True:
                    self.deselect()

            # DESELEZIONE CLICCANDO AL DI FUORI DI SE STESSO
            else:
                for cell in Main.hex_cells:
                    if cell.checkHexMousecollision() != None:
                        if cell.dts > self.movepts:
                            if Main.controller.selectedd == self:
                                self.deselect()

                        elif cell.dts <= self.movepts and cell.occupied == True:
                            for player in Main.players:
                                for unit in player.units:
                                    if (
                                        unit.parentcell == cell
                                        and cell.dts > self.atkrange
                                    ):
                                        if unit.activated == False:
                                            if Main.controller.selectedd == self:
                                                self.deselect()
        # SELEZIONE PER AI
        elif (
            self.ai == True
            and self.moving == False
            and Main.controller.actingUnit == None
        ):
            if Main.controller.ai_selected == self and self.aiFinishedTurn == False:
                self.selected = True
                Main.controller.selectedd = self
                for cell in Main.hex_cells:
                    cell.dts = 999
                self.getParentCell()
                if self.moved == False:
                    self.recalculateDts()
            else:
                self.selected = False

    # move
    def move(self):
        if not self.ai:
            if (
                Main.controller.selectedd == self
                and self.movepts > 0
                and not self.moved
                and self.activated
                and self.attacked_target == None
            ):
                for cell in Main.hex_cells:
                    if (
                        cell.checkHexMousecollision() is not None
                        and cell != self.parentcell
                        and cell.dts <= self.movepts
                        and not cell.occupied
                    ):
                        # flip img
                        mouse_pos = pygame.mouse.get_pos()

                        if mouse_pos[0] < self.x and self.flipChecker == False:
                            self.flipImage()
                            self.flipChecker = True

                        elif mouse_pos[0] > self.x and self.flipChecker == True:
                            print("ciao")
                            self.flipImage()

                            self.flipChecker = False
                        else:
                            pass

                        self.movepts -= cell.dts
                        self.move_target = cell

                        # print("remaining movement points are " + str(self.movepts))

        elif self.ai:
            if (
                Main.controller.selectedd == self
                and self.movepts > 0
                and not self.moved
                and self.activated
                and self.attacked_target == None
            ):
                nearestCellToEnemy = self.aiCalculateNearestCellToNearestEnemy()
                if (
                    nearestCellToEnemy is not None
                    and nearestCellToEnemy != self.parentcell
                    and nearestCellToEnemy.dts <= self.movepts
                    and nearestCellToEnemy.occupied == False
                ):
                    # flip image
                    if (
                        nearestCellToEnemy.center[0] > self.x
                        and self.flipChecker == False
                    ):
                        self.flipImage()
                        self.flipChecker = True
                    elif (
                        nearestCellToEnemy.center[0] < self.x
                        and self.flipChecker == True
                    ):
                        self.flipImage()
                        self.flipChecker = False
                    else:
                        pass

                    nearestCellToEnemy.occupied = True
                    self.movepts -= nearestCellToEnemy.dts
                    self.move_target = nearestCellToEnemy

                    # print("ai remaining movement points are " + str(self.movepts))

    # move animation
    def moveAnimation(self):
        if self.moved:
            for cell in Main.hex_cells:
                cell.dts = 999
            self.getParentCell()
            self.createMask()
            self.move_target = None

            self.recalculateDts()
            """ for cell in Main.hex_cells:
                        while cell.dts == 999:
                            for hex in Main.hex_cells:
                                hex.dtsf() """

            self.moving = False
            # print('movimento finito')
            Main.controller.actingUnit = None
            self.moved = False

        if self.move_target != None:
            if Main.controller.actingUnit == None or Main.controller.actingUnit == self:
                path = pygame.math.Vector2(0, 0)
                direction_x = self.move_target.center[0] - self.x
                direction_y = self.move_target.center[1] - self.y

                length = pygame.math.Vector2(direction_x, direction_y).length()

                # se la distanza è maggiore del pezzetto di movimento mi muovo del pezzetto per intero
                if (
                    length != 0
                    and length
                    > pygame.math.Vector2(
                        direction_x / length, direction_y / length
                    ).length()
                    * Main.speed
                ):
                    Main.controller.actingUnit = self
                    path = pygame.math.Vector2(
                        direction_x / length, direction_y / length
                    )
                    self.moving = True
                    self.x += path[0] * Main.speed
                    self.y += path[1] * Main.speed

                # se la distanza è minore del pezzetto vado diretto al punto
                else:
                    # path = pygame.math.Vector2(0, 0)
                    self.x = self.move_target.center[0]
                    self.y = self.move_target.center[1]

                    self.moved = True
                    self.moving = True
                    # print('arrived')

                self.getCenter(self.x, self.y)

    # attack
    def attack(self):
        if not self.ai:
            for player in Main.players:
                for unit in player.units:
                    if (
                        not unit.activated
                        and unit.parentcell.dts <= self.atkrange
                        and unit.parentcell.checkHexMousecollision() is not None
                        and self.activated
                        and Main.controller.selectedd == self
                        and self.atkpts
                    ):
                        # flip image
                        if unit.x < self.x and self.flipChecker == False:
                            self.flipImage()
                            self.flipChecker = True
                        elif unit.x > self.x and self.flipChecker == True:
                            self.flipImage()
                            self.flipChecker = False
                        else:
                            pass

                        self.start_x = self.x
                        self.start_y = self.y
                        self.attacked_target = unit  # per l'animazione di attacco
                        self.middle = self.calculateMidPoint()
                        unit.hp -= self.atk
                        self.atkpts -= 1
                        if unit.hp <= 0:
                            Main.controller.kill(unit)
        elif self.ai:
            enemy = self.aiCalculateNearestEnemy()

            if (
                enemy.parentcell.dts <= self.atkrange
                and self.atkpts > 0
                and Main.controller.ai_selected == self
                and self.selected
            ):
                # flip image
                if enemy.x > self.x and self.flipChecker == False:
                    self.flipImage()
                    self.flipChecker = True
                elif enemy.x < self.x and self.flipChecker == True:
                    increment = 0
                    self.flipImage()
                    self.flipChecker = False
                else:
                    pass

                self.start_x = self.x
                self.start_y = self.y
                self.attacked_target = enemy  # per l'animazione di attacco
                self.middle = self.calculateMidPoint()
                enemy.hp -= self.atk
                self.atkpts -= 1
                if enemy.hp <= 0:
                    Main.controller.kill(enemy)

    # calcola il punto medio
    def calculateMidPoint(self):
        middle = [
            (self.x + self.attacked_target.x) / 2,
            (self.y + self.attacked_target.y) / 2,
        ]
        return middle

    # attack animation
    def attackAnimation(self, animSpeed):
        if self.attacked_target != None:
            if Main.controller.actingUnit == None or Main.controller.actingUnit == self:
                # print(self.x, self.middle[0],self.attacked_target.x)

                if self.attacked_target_returning == False:
                    Main.controller.actingUnit = self
                    # print('attacked_target_returning=false')
                    direction = pygame.math.Vector2(
                        self.middle[0] - self.x, self.middle[1] - self.y
                    )
                    length = pygame.math.Vector2(direction).length()
                    if length != 0:
                        direction /= length
                    if length > pygame.math.Vector2(direction).length() + animSpeed:
                        # print('1')
                        self.x += direction[0] * animSpeed
                        self.y += direction[1] * animSpeed

                    elif length <= pygame.math.Vector2(direction).length() + animSpeed:
                        # print('2')
                        self.x = self.middle[0]
                        self.y = self.middle[1]

                        self.attacked_target_returning = True

                elif self.attacked_target_returning == True:
                    Main.controller.actingUnit = self
                    # print('attacked_target_returning=true')
                    direction = pygame.math.Vector2(
                        self.start_x - self.x, self.start_y - self.y
                    )
                    length = pygame.math.Vector2(direction).length()
                    # print (length)
                    # print(pygame.math.Vector2(direction[0],direction[1]).length())
                    if length != 0:
                        direction /= length

                    if (
                        length
                        > pygame.math.Vector2(direction[0], direction[1]).length()
                        + animSpeed
                    ):
                        # print('3')
                        self.x += direction[0] * animSpeed
                        self.y += direction[1] * animSpeed

                    elif (
                        length
                        <= pygame.math.Vector2(direction[0], direction[1]).length()
                        + animSpeed
                    ):
                        # print('4')
                        self.x = self.start_x
                        self.y = self.start_y
                        self.attacked_target = None
                        self.attacked_target_returning = False
                        self.start_x = 0
                        self.start_y = 0
                        self.createMask()
                        Main.controller.actingUnit = None

                self.getCenter(self.x, self.y)

    def aiEndTurn(self):
        enemy = self.aiCalculateNearestEnemy()
        if (
            enemy.parentcell.dts > self.atkrange
            and self.movepts == 0
            and Main.controller.actingUnit == None
            and Main.controller.ai_selected == self
        ):
            print(f"{enemy.parentcell.dts}, {self.atkrange}")
            print("finished")
            self.aiFinishedTurn = True

        if self.atkpts == 0 and Main.controller.actingUnit == None:
            print("finished in da other wae")
            self.aiFinishedTurn = True

    # ai_calcolo il nemico + vicino
    def aiCalculateNearestEnemy(self):
        enemies = []
        enemies_dist = []
        for player in Main.players:
            for unit in player.units:
                if unit.activated == False:
                    enemies.append(unit)
                    enemies_dist.append(Main.dist(unit.x, self.x, unit.y, self.y))
        enemies_dist.sort()
        for en in enemies:
            if Main.dist(en.x, self.x, en.y, self.y) == enemies_dist[0]:
                # print("target acquired!")
                return en

    # ai_calcolo la cella in range di movimento più vicina al nearest enemy
    def aiCalculateNearestCellToNearestEnemy(self):
        nearest = self.aiCalculateNearestEnemy()
        CellsWhereAIcanMove = []
        CellsWhereAIcanMove_dist = []
        Main.controller.checkOccupiedCells()
        for cell in Main.hex_cells:
            if (
                cell.dts <= self.movepts
                and cell.occupied == False
                and cell not in CellsWhereAIcanMove
                and nearest.parentcell.dts > self.atkrange
            ):
                CellsWhereAIcanMove.append(cell)
                CellsWhereAIcanMove_dist.append(
                    Main.dist(cell.center[0], nearest.x, cell.center[1], nearest.y)
                )
        CellsWhereAIcanMove_dist.sort()
        for hex in CellsWhereAIcanMove:
            if (
                Main.dist(hex.center[0], nearest.x, hex.center[1], nearest.y)
                == CellsWhereAIcanMove_dist[0]
            ):
                return hex

    def flipImage(self):
        if self.img[0] != None:
            self.img[0] = pygame.transform.flip(self.img[0], True, False)

        if self.img[1] != None:
            self.img[1] = pygame.transform.flip(self.img[1], True, False)

        if self.img[2] != None:
            self.img[2] = pygame.transform.flip(self.img[2], True, False)

        if self.img[3] != None:
            self.img[3] = pygame.transform.flip(self.img[3], True, False)

    def applyRaceModifiers(self):
        # imposto le statistiche di base in base alla razza
        if self.race == "human":
            self.img[1] = pygame.image.load("./media/races/human/human_base_body_0.png")
            self.orig_img[1] = self.img[1]
            self.img[2] = pygame.image.load("./media/races/human/human_base_head_0.png")
            self.orig_img[2] = self.img[2]
            self.hp += 2
            self.maxhp += 2
            self.movepts += 1
            self.totmovepts += 1

        elif self.race == "orc":
            self.img[1] = pygame.image.load("./media/races/orc/orc_base_body_0.png")
            self.orig_img[1] = self.img[1]
            self.img[2] = pygame.image.load("./media/races/orc/orc_base_head_0.png")
            self.orig_img[2] = self.img[2]
            self.hp += 2
            self.maxhp += 2
            self.atk += 1

        elif self.race == "goblin":
            self.img[1] = pygame.image.load(
                "./media/races/goblin/goblin_base_body_0.png"
            )
            self.orig_img[1] = self.img[1]
            self.img[2] = pygame.image.load(
                "./media/races/goblin/goblin_base_head_0.png"
            )
            self.orig_img[2] = self.img[2]
            self.atkpts += 1
            self.movepts += 2
            self.totmovepts += 2

        elif self.race == "dwarf":
            self.img[1] = pygame.image.load("./media/races/dwarf/dwarf_base_body_0.png")
            self.orig_img[1] = self.img[1]
            self.img[2] = pygame.image.load("./media/races/dwarf/dwarf_base_head_0.png")
            self.orig_img[2] = self.img[2]
            self.hp += 3
            self.maxhp += 3

        elif self.race == "elf":
            self.img[1] = pygame.image.load("./media/races/orc/orc_base_body_0.png")
            self.orig_img[1] = self.img[1]
            self.hp += 1
            self.maxhp += 1
            self.movepts += 1
            self.totmovepts += 1
            self.atkpts += 1

        else:
            pass

        if self.ai == True:
            self.flipImage()
        self.createMask()

    def applyEquipmentModifiers(self):
        # resetto i modifiers (senno me li aggiunge a quelli che c'erao gia prima)
        self.hp = self.basestats[0]
        self.maxhp = self.hp
        self.atk = self.basestats[1]
        self.atkpts = self.basestats[2]
        self.totatkpts = self.atkpts
        self.movepts = self.basestats[3]
        self.totmovepts = self.movepts
        self.atkrange = self.basestats[4]

        for part in self.inventory.values():
            for group in equipment.all.values():
                for equipo in group.keys():
                    if part == equipo:
                        # aggiorno le statistiche
                        self.hp += group[equipo][0]
                        self.maxhp += group[equipo][0]
                        self.atk += group[equipo][1]
                        self.movepts += group[equipo][2]
                        self.totmovepts += group[equipo][2]
                        self.atkpts += group[equipo][3]
                        self.totatkpts += group[equipo][3]
                        self.atkrange += group[equipo][4]

                        # cambio l'immagine del'omino in base all'equipaggiamento
                        for key in equipment.all.keys():
                            for ke in self.inventory.keys():
                                if equipment.all[key] == group and ke == key:
                                    if key == "lhand":
                                        self.img[0] = group[equipo][6]
                                        # inverto l'immagine dell'equip se di ai
                                        if self.ai == True and self.img[0] != None:
                                            self.img[0] = pygame.transform.flip(
                                                self.img[0], True, False
                                            )

                                    elif key == "body":
                                        self.img[1] = group[equipo][6]
                                        if self.ai == True and self.img[1] != None:
                                            self.img[1] = pygame.transform.flip(
                                                self.img[1], True, False
                                            )

                                    elif key == "head":
                                        self.img[2] = group[equipo][6]
                                        if self.ai == True and self.img[2] != None:
                                            self.img[2] = pygame.transform.flip(
                                                self.img[2], True, False
                                            )

                                    elif key == "rhand":
                                        self.img[3] = group[equipo][6]
                                        if self.ai == True and self.img[3] != None:
                                            self.img[3] = pygame.transform.flip(
                                                self.img[3], True, False
                                            )
                                    else:
                                        pass

        self.createMask()

        """ self.img[0]=self.inventory['body']
        self.img[1]=self.inventory['rhand']
        self.img[2]=self.inventory['lhand']
        self.img[3]=self.inventory['head']
                 """
