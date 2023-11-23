import Main
import unitt
import random
import equipment

class Player:
    def __init__(self, points,ai):
        self.points = points  # punti per la selezione e creazone di unità del giocatore
        self.units_inventory = []  # lista delle unità in possesso del giocatore
        self.units = []  # lista delle unità del giocatore attualmente attive in gioco
        self.ai=ai

    def ai_turn_end_control(self):

        for unit in self.units:
            
            if unit.aiFinishedTurn == True and self.units.index(unit)+1 == len(self.units):
                #print('yes')
                Main.controller.turnEnd()
                #print('yes2')
   
    def ai_units_random_choice(self):
        #compro le unita
        if self.points>0 and self.ai==True:
            a=Main.units_type_INVENTORY[random.randrange(0, len(Main.units_type_INVENTORY))]
            new_unit=unitt.Unit(True,a.id,a.nome,a.race) 
            for i in new_unit.img:
                for j in a.img:
                    for d in range(3):
                        if new_unit.img[d]==i and a.img[d]==j:
                            i=j
            

            #compro dell'equipaggiamento casuale
            for i in new_unit.inventory.keys():
                for j in equipment.all.keys():
                       
                        if j==i and new_unit.inventory[j] != None:
                            
                            chiavi=list(equipment.all[j].keys())
                            if chiavi != []:
                                
                                indice_casuale=random.randint(0,len(chiavi)-1)
                                if new_unit.race in chiavi[indice_casuale]:
                                    if i=='rhand' and new_unit.animation[0]!=None and new_unit.animation[0][-4]==True:
                                        pass
                                    else:
                                        new_unit.inventory[j]=chiavi[indice_casuale]
                                
                                        self.points-=equipment.all[j][chiavi[indice_casuale]][5] #costo dell equipaggiamento

            new_unit.applyEquipmentModifiers()
           
            self.points-=5
            self.units.append(new_unit)
            new_unit.id=self.units.index(new_unit)
            #print('le unità appartenenti all ai sono: ',self.units)

 

           