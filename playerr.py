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
        self.ai_selection_ended=False

    def ai_turn_end_control(self):

        for unit in self.units:
            
            if unit.aiFinishedTurn == True and self.units.index(unit)+1 == len(self.units):
                #print('yes')
                Main.controller.turnEnd()
                #print('yes2')
   
    def ai_units_random_choice(self):
        #compro le unita
        if self.ai==True:
            if (self.points-5)>0:
                a=Main.units_type_INVENTORY[random.randrange(0, len(Main.units_type_INVENTORY))]
                new_unit=unitt.Unit(True,a.id,a.nome,a.race) 
                """ for i in new_unit.img:
                    for j in a.img:
                        for d in range(3):
                            if new_unit.img[d]==i and a.img[d]==j:
                                i=j """
                
                random_ordered_inventory=list(new_unit.inventory.items())
                random.shuffle(random_ordered_inventory)
                shuffled_inventory=dict(random_ordered_inventory)
                self.points-=5
                #compro dell'equipaggiamento casuale
                for i in shuffled_inventory.keys():
                    
                    if new_unit.inventory[i]=="" and self.points>0:
                            
                        if i=="rhand" and new_unit.animation[0]!=None and new_unit.animation[0][-4]==True:
                            pass
                        elif i=="lhand" and new_unit.animation[3]!=None and new_unit.animation[3][-4]==True:
                            pass
                        else:
                            for j in equipment.all.keys():
                                
                                    if j==i:
                                        
                                        """ chiavi=list(equipment.all[j].keys())
                                        race_keys=[] """
                                        elems=list(equipment.all[j].items())
                                        
                                        
                                        random.shuffle(elems)
                                        shuffled_part=dict(elems)
                                        
                                        for k in shuffled_part.keys():
                                            
                                            if new_unit.race in k:
                                                

                                                if i=='lhand' and new_unit.inventory['rhand']!="" and equipment.all[j][k][7][-1]==True:
                                                    pass
                                                elif i=='rhand' and new_unit.inventory['lhand']!="" and equipment.all[j][k][7][-1]==True:
                                                    pass
                                                else:
                                                    if self.points-equipment.all[j][k][5]>=0:
                                                        new_unit.inventory[j]=k
                                                
                                                        self.points-=equipment.all[j][k][5] #costo dell equipaggiamento
                                                        print(self.points,equipment.all[j][k][5])
                                                        break
                                                    
                            new_unit.applyEquipmentModifiers()
                            
                
            
                if self.points>=0:
                    self.units.append(new_unit)
                    
                    new_unit.id=self.units.index(new_unit)
                #print('le unità appartenenti all ai sono: ',self.units)

            else:
                self.ai_selection_ended=True

           