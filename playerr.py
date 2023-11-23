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
            """ for i in new_unit.img:
                for j in a.img:
                    for d in range(3):
                        if new_unit.img[d]==i and a.img[d]==j:
                            i=j """
            

            #compro dell'equipaggiamento casuale
            for i in new_unit.inventory.keys():
               print(i)
               if new_unit.inventory[i]=="":
                    
                    if i=="rhand" and new_unit.animation[0]!=None and new_unit.animation[0][-4]==True:
                        print('2handed')
                        pass
                    else:
                        for j in equipment.all.keys():
                            
                                if j==i:
                                    
                                    chiavi=list(equipment.all[j].keys())
                                    race_keys=[]
                                    for keyy in chiavi:
                                        if new_unit.race in keyy:
                                            race_keys.append(keyy)

                                    indice_casuale=random.randint(0,len(race_keys)-1)
                                            
                                    if new_unit.race in race_keys[indice_casuale]:
                                        
                                        
                                            new_unit.inventory[j]=race_keys[indice_casuale]
                                    
                                            self.points-=equipment.all[j][chiavi[indice_casuale]][5] #costo dell equipaggiamento
                        new_unit.applyEquipmentModifiers()
            
           
            self.points-=5
            self.units.append(new_unit)
            new_unit.id=self.units.index(new_unit)
            #print('le unità appartenenti all ai sono: ',self.units)

 

           