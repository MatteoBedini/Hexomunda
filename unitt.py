import pygame
import Main
import equipment




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
        self.orig_img = [None, None, None, None]  # template [lhand,body,head,rhand]

        
        self.animation = [None, None, None, None]
        self.animated = False
        

        self.flipChecker = False
        # self.getCenter(self.x, self.y)

        # statistiche di gioco
        self.hp = 1
        self.maxhp = 1

        self.totmovepts = 1
        self.movepts = 1
        self.cells_where_can_move=[]

        self.atk = 1
        self.atkpts = 1
        self.totatkpts = self.atkpts
        self.atkrange = 1
        self.atkOpportunityCheck=False

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
            "lhand": "",
            "body": "",
            "head": "",
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

    def controlAnimation(self,img):
        #img[-1]= elapsed time
        #img[-2]= animation speed
        #img[-3]= current frame
        

        #img[-4]= frame number
        #img[0]= animation list
        img[-1] += Main.clock.get_rawtime()  #images specific elapsed time
        
        if img[-1] >= img[-2]* 1000:  #animation speed
            if img[-3] >= len(img[0]) - 1:
                img[-3] = 0
                
            else:
                img[-3] += 1
                
            img[-1] = 0

        return img[0][img[-3]]
    
    def makeItGlow(self,screen):
        mouse_pos = pygame.mouse.get_pos()
        # illumino l'omino in base alla maschera se ci passo sopra col mouse
        if self.rectMask.collidepoint(mouse_pos[0], mouse_pos[1]) == True:
            for d in range(0,len(self.glow)):  
                if self.glow[d] != None:
                    i=self.animation[d][-3]
                    for dot in self.glow[d][i]:
                        pygame.draw.rect(
                            screen,
                            (216, 235, 246,150),
                            pygame.Rect(
                                dot[0] + self.center[0]-1,
                                dot[1] + self.center[1]-1,
                                3,
                                3,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (216, 235, 246,150),
                            pygame.Rect(
                                dot[0] + self.center[0]-1 + 1,
                                dot[1] + self.center[1]-1,
                                3,
                                3,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (216, 235, 246,150),
                            pygame.Rect(
                                dot[0] + self.center[0]-1 - 1,
                                dot[1] + self.center[1]-1,
                                3,
                                3,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (216, 235, 246,150),
                            pygame.Rect(
                                dot[0] + self.center[0]-1,
                                dot[1] + self.center[1]-1 - 1,
                                3,
                                3,
                            ),
                        )
                        pygame.draw.rect(
                            screen,
                            (216, 235, 246,150),
                            pygame.Rect(
                                dot[0] + self.center[0]-1,
                                dot[1] + self.center[1]-1 + 1,
                                2,
                                2,
                            ),
                    )

    # disegno
    def draw(self, screen):
        if Main.room.roomNumber != 1:
            self.makeItGlow(screen)
        
        # UNIT DRAW
        
        if self.animated==True:
            for img_counter in range(0, len(self.animation)):
                if self.animation[img_counter] != None:
                    
                    
                    to_be_drawn=self.controlAnimation(self.animation[img_counter])
                    
                    screen.blit(
                        to_be_drawn,
                        (
                            self.center[0],
                            self.center[1],
                        ),
                    )
                    
                else:

                    if self.img[img_counter] != None:
                        
                            
                            screen.blit(
                                self.img[img_counter],
                                (
                                    self.center[0],
                                    self.center[1],
                                ),
                            )
        else:
            for i in self.img:
                if i != None:
                    screen.blit(
                        i,
                        (
                            self.center[0],
                            self.center[1],
                        ),
                    )

        # se siamo nella room di gioco degli esagoni faccio vedere la barra della vita
        if Main.room.roomNumber == 2:
            self.drawHpBar(screen, 40, 7*Main.zoom, self.center[0], self.center[1])

    # sottometodo:disegno la barra della vita
    def drawHpBar(self, screen, max, height, x, y):
        hpPercentage = self.hp * 100 / self.maxhp
        rectMaxLength = max*Main.zoom
        rectWidth = rectMaxLength * hpPercentage / 100
        if self.ai == True:
            pygame.draw.rect(
                screen,
                (242, 39, 39),
                (
                    x - rectMaxLength/2 + self.img[1].get_width()/2,
                    
                    y + 4,
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
                    x - rectMaxLength/2 + self.img[1].get_width()/2,
                    y + 4,
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
                    x - rectMaxLength/2 + self.img[1].get_width()/2,
                    y + 4,
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
                    x - rectMaxLength/2 + self.img[1].get_width()/2,
                    y + 4,
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
                x - rectMaxLength / 4 + self.img[1].get_width()/2,
                y - 6,
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

        self.mask=[None,None,None,None]
        self.glow=[None,None,None,None]
        if self.animated==True:
            #creo la maschera
            for img_counter in range(0, len(self.animation)):
                if self.animation[img_counter] != None:
                    self.mask[img_counter] = []
                    for i in range(len(self.animation[img_counter][0])):
                        self.mask[img_counter].append(pygame.mask.from_surface(
                            self.animation[img_counter][0][i]
                        ))

                else:

                    if self.img[img_counter] != None:
                        self.mask[img_counter] = pygame.mask.from_surface(
                            self.img[img_counter]
                        )
            #creo l'outline
            for img_counter in range(0, len(self.mask)):
                if self.mask[img_counter] != None:
                    self.glow[img_counter] = []
                    for i in range(len(self.mask[img_counter])):
                        self.glow[img_counter].append((self.mask[img_counter][i].outline()))
        
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
            if cell.dts<=self.movepts and cell not in self.cells_where_can_move:
                self.cells_where_can_move.append(cell)
                  
        if all(cell.dts != 999 for cell in Main.hex_cells):
            for cell in Main.hex_cells:
                

                cell.checkForBarrier()
            
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

                    self.cells_where_can_move = []
                    if self.moved == False:
                        self.recalculateDts()
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
                self.cells_where_can_move = []
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
                        and not cell.blockedForMovement
                    ):
                        # flip img
                        mouse_pos = pygame.mouse.get_pos()

                        if mouse_pos[0] < self.x and self.flipChecker == False:
                            self.flipImage()
                            self.flipChecker = True

                        elif mouse_pos[0] > self.x and self.flipChecker == True:

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
                cell.blockedForMovement = False
                cell.dts = 999
            
            self.getParentCell()
            self.createMask()
            self.move_target = None

            #self.recalculateDts()
 
            self.moving = False
            # print('movimento finito')
            Main.controller.actingUnit = None
            Main.controller.checkOccupiedCells()
            self.cells_where_can_move = []
            self.recalculateDts()
 
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
                        if self.atkrange<2:
                            Main.controller.atkedUnit=unit
                            Main.controller.img=equipment.atk_animation
                        else:
                           Main.controller.rngAtkedUnit=unit
                           Main.controller.img=equipment.ranged_atk_animation
                        self.middle = self.calculateMidPoint()
                        unit.hp -= self.atk
                        self.atkpts -= 1
                        if unit.hp <= 0:
                            Main.controller.kill(unit)
        elif self.ai:
            enemy = self.aiCalculateNearestEnemy()

            if (
                enemy!=None
                and enemy.parentcell.dts <= self.atkrange
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
                if self.atkrange<2:
                    Main.controller.atkedUnit=enemy
                    Main.controller.img=equipment.atk_animation
                else:
                    Main.controller.rngAtkedUnit=enemy
                    Main.controller.img=equipment.ranged_atk_animation
                self.middle = self.calculateMidPoint()
                enemy.hp -= self.atk
                self.atkpts -= 1
                if enemy.hp <= 0:
                    Main.controller.kill(enemy)

    
    def attackOfOpportunity(self):
        if self.parentcell!=None:
            if self.parentcell.dts ==1 and Main.controller.selectedd != None and Main.controller.selectedd.move_target != None and not self.activated and self.atkOpportunityCheck==False:
                
                self.atkOpportunityCheck=True
            # flip image
                if Main.controller.selectedd.x > self.x and self.flipChecker == False:
                    self.flipImage()
                    self.flipChecker = True
                elif Main.controller.selectedd.x < self.x and self.flipChecker == True:
                    increment = 0
                    self.flipImage()
                    self.flipChecker = False
                else:
                    pass

                self.start_x = self.x
                self.start_y = self.y
                self.attacked_target = Main.controller.selectedd  # per l'animazione di attacco
                if self.atkrange<2:
                    Main.controller.atkedUnit=Main.controller.selectedd
                    Main.controller.img=equipment.atk_animation
                else:
                    Main.controller.rngAtkedUnit=Main.controller.selectedd
                    Main.controller.img=equipment.ranged_atk_animation
                self.middle = self.calculateMidPoint()
                Main.controller.selectedd.hp -= self.atk
                self.atkpts -= 1
                if Main.controller.selectedd.hp <= 0:
                    Main.controller.kill(Main.controller.selectedd)
                    Main.controller.selectedd = None
                    Main.controller.actingUnit = None

    # calcola il punto medio
    def calculateMidPoint(self):
        middle = [
            (self.x + self.attacked_target.x) / 2,
            (self.y + self.attacked_target.y) / 2,
        ]
        return middle

    # attack animation
    def attackAnimation(self, animSpeed):
        if self.attacked_target != None and self.atkrange==1:
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
        else:
            self.attacked_target = None

    def aiEndTurn(self):
        enemy = self.aiCalculateNearestEnemy()
        if enemy == None:
           self.aiFinishedTurn = True
           Main.room.roomNumber=6
           return 
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
            if player.units != []:
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
                and not cell.blockedForMovement 
            ):
                if nearest.parentcell.dts-cell.dts>=self.atkrange:
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
        if self.animation[0]!=None:
            for i in range(len(self.animation[0][0])):
                self.animation[0][0][i]=pygame.transform.flip(self.animation[0][0][i], True, False)
        if self.animation[1]!=None:
            for i in range(len(self.animation[1][0])):
                self.animation[1][0][i]=pygame.transform.flip(self.animation[1][0][i], True, False)
        if self.animation[2]!=None:
            for i in range(len(self.animation[2][0])):
                self.animation[2][0][i]=pygame.transform.flip(self.animation[2][0][i], True, False)
        if self.animation[3]!=None:
            for i in range(len(self.animation[3][0])):
                self.animation[3][0][i]=pygame.transform.flip(self.animation[3][0][i], True, False)
            
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
            self.animated=True
            self.animation[1] = equipment.loadAnimation("./media/races/human/animations/",
                                                  "human_base_body_0",4)

            self.img[1] = pygame.image.load("./media/races/human/human_base_body_0.png")
            self.orig_img[1] = self.img[1]

            self.animation[2] = equipment.loadAnimation("./media/races/human/animations/",
                                                  "human_base_head_0",4)
            self.img[2] = pygame.image.load("./media/races/human/human_base_head_0.png")
            self.orig_img[2] = self.img[2]

            self.hp += 2
            self.maxhp += 2
            self.movepts += 1
            self.totmovepts += 1

        elif self.race == "orc":
            self.animated=True
            self.animation[1] = equipment.loadAnimation("./media/races/orc/animations/",
                                                  "orc_base_body_0",4)

            self.img[1] = pygame.image.load("./media/races/orc/orc_base_body_0.png")
            self.orig_img[1] = self.img[1]

            self.animation[2] = equipment.loadAnimation("./media/races/orc/animations/",
                                                  "orc_base_head_0",4)
            self.img[2] = pygame.image.load("./media/races/orc/orc_base_head_0.png")
            self.orig_img[2] = self.img[2]
            self.hp += 2
            self.maxhp += 2
            self.atk += 1

        elif self.race == "goblin":
            self.animated=True
            self.animation[1] = equipment.loadAnimation("./media/races/goblin/animations/",
                                                  "goblin_base_body_0",4)
            self.img[1] = pygame.image.load(
                "./media/races/goblin/goblin_base_body_0.png"
            )
            self.orig_img[1] = self.img[1]
            self.animation[2] = equipment.loadAnimation("./media/races/goblin/animations/",
                                                  "goblin_base_head_0",4)
            self.img[2] = pygame.image.load(
                "./media/races/goblin/goblin_base_head_0.png"
            )
            self.orig_img[2] = self.img[2]
            #self.atkpts += 1
            self.movepts += 2
            self.totmovepts += 2

        elif self.race == "dwarf":
            self.animated=True
            self.animation[1] = equipment.loadAnimation("./media/races/dwarf/animations/",
                                                  "dwarf_base_body_0",4)
            self.img[1] = pygame.image.load("./media/races/dwarf/dwarf_base_body_0.png")
            self.orig_img[1] = self.img[1]

            self.animation[2] = equipment.loadAnimation("./media/races/dwarf/animations/",
                                                  "dwarf_base_head_0",4)
            self.img[2] = pygame.image.load("./media/races/dwarf/dwarf_base_head_0.png")
            self.orig_img[2] = self.img[2]
            self.hp += 4
            self.maxhp += 4

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
                                        if group[equipo][7] != None:
                                            self.animation[0]=equipment.loadAnimation(*group[equipo][7])  #*asterisco prima del nome della variabile per fare un unpack della tupla

                                    elif key == "body":
                                        self.img[1] = group[equipo][6]
                                        if group[equipo][7] != None:
                                            self.animation[1]=equipment.loadAnimation(*group[equipo][7])
                                        
                                    elif key == "head":
                                        self.img[2] = group[equipo][6]
                                        if group[equipo][7] != None:
                                            self.animation[2]=equipment.loadAnimation(*group[equipo][7])

                                    elif key == "rhand":
                                        self.img[3] = group[equipo][6]
                                        if group[equipo][7] != None:
                                            self.animation[3]=equipment.loadAnimation(*group[equipo][7])

                                    else:
                                        pass

        self.createMask()


        
                                     
       

                    

                

