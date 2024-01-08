import pygame
import Main
import equipment
import unitt

class Inanimated:
    def __init__(self,nome):
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
        self.img=None

        # maschera
        self.rectMask = []
        self.mask=[None,None,None,None]
        self.glow=[None,None,None,None]

        # hexcell di locazione
        self.rectForParent = None  # rettangolino per centrare l'unita nell'esagono
        self.parentcell = None
        self.getParentCell()


    def getCenter(self, x, y):
        self.center[0] = x - ((self.img.get_width()) / 2)
        self.center[1] = y - ((self.img.get_height()) / 2)

    def draw(self, screen):
        #mouse_pos = pygame.mouse.get_pos()
        #illumino l'omino in base alla maschera se ci passo sopra col mouse
        """ if self.rectMask.collidepoint(mouse_pos[0], mouse_pos[1]) == True:
                if self.glow != None:
                    for dot in self.glow:
                        pygame.draw.rect(screen, (247, 247, 247), pygame.Rect(dot[0]+self.center[0], dot[1]+self.center[1], 1, 1))
                        pygame.draw.rect(screen, (247, 247, 247), pygame.Rect(dot[0]+self.center[0]+1, dot[1]+self.center[1], 1, 1))
                        pygame.draw.rect(screen, (247, 247, 247), pygame.Rect(dot[0]+self.center[0]-1, dot[1]+self.center[1], 1, 1))
                        pygame.draw.rect(screen, (247, 247, 247), pygame.Rect(dot[0]+self.center[0], dot[1]+self.center[1]-1, 1, 1))
                        pygame.draw.rect(screen, (247, 247, 247), pygame.Rect(dot[0]+self.center[0], dot[1]+self.center[1]+1, 1, 1)) """
                
        #disegno l'omino
        screen.blit(self.img, (self.center[0], self.center[1]-20))

    def getParentCell(self):
        self.rectForParent = pygame.Rect((self.x - 5, self.y - 5), (10, 10))

        for cell in Main.hex_cells:
            if self.rectForParent.collidepoint(cell.center[0], cell.center[1]) == True:
                self.parentcell = cell

        if Main.controller.selectedd == self and self.parentcell != None:
            #print("yes parent cell dts is set to zero ")
            self.parentcell.dts = 0

    def createMask(self):
        self.rectMask = pygame.Rect(
            self.center[0], self.center[1], self.img.get_width(), self.img.get_height()
        )
        self.mask=pygame.mask.from_surface(self.img)
        self.glow=self.mask.outline()

        