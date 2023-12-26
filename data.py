import json
import os
import Main
from unitt import Unit
import copy

def update():
   units1=[]
   units2=[]
   for player in Main.players:
       for unit in player.units:
           un=[
               unit.id, 
               unit.nome,
               unit.x,
               unit.y,
               unit.col,
               unit.row,
               unit.center,
               unit.animated,
               unit.flipChecker,
               unit.hp,
               unit.maxhp,
               unit.totmovepts,
               unit.movepts,
               unit.atk,
               unit.atkpts,
               unit.totatkpts,
               unit.atkrange,
               unit.atkOpportunityCheck,
               unit.ai,
               unit.inventory,
               #unit.img,
               #unit.orig_img,
               #unit.animation,
               unit.activated,
               unit.selected,
               unit.move_target,
               unit.moving,
               unit.moved,
               unit.attacked_target,
               unit.middle,
               unit.start_x,
               unit.start_y,
               unit.attacked_target_returning,
               unit.race,
               unit.basestats,
               unit.aiFinishedTurn,

           ]
           if player.ai==True:
                units2.append(un)
           else:
                units1.append(un)
           

   return {
    'controller':[{
        'game phase':Main.controller.gameFase
    }
    ],
    'players':[ 
        {
            'name':'player',
            'points':Main.players[0].points,
            'units':units1,

        },
        {
            'name':'ai_player',
            'points':Main.players[1].points,
            'units':units2,
        }
    ]
}

def save():
    if not os.path.exists('./saved_games'):
        os.makedirs('./saved_games')

    files_counter=0
    files = [f for f in os.listdir('./saved_games') if os.path.isfile(os.path.join('./saved_games', f))]
    for filee in files:
        files_counter+=1
    with open(f'./saved_games/save_'+str(files_counter)+'.json', 'w') as outfile:
        json.dump(update(), outfile)
    print('file saved')

def load(savefile):
    data = None
    with open(f'./saved_games/{savefile}', 'r') as outfile:
        data = json.load(outfile)
    print(data)

    Main.players[0].points=data['players'][0]['points']
    Main.players[1].points=data['players'][1]['points']
    
    for unit in data['players'][0]['units']:
        new_unit=Unit(False,1,'','human')
        new_unit.id=unit[0]
        new_unit.nome=unit[1]
        new_unit.x=unit[2]
        new_unit.y=unit[3]
        new_unit.col=unit[4]
        new_unit.row=unit[5]
        new_unit.center=unit[6]
        new_unit.animated=unit[7]
        new_unit.flipChecker=unit[8]
        new_unit.atkOpportunityCheck=unit[17]
        new_unit.ai=unit[18]
        new_unit.inventory=unit[19]
        new_unit.activated=unit[20]
        new_unit.selected=unit[21]
        new_unit.moving=unit[23]
        new_unit.moved=unit[24]
        new_unit.race=unit[30]
        new_unit.basestats=unit[31]
        new_unit.aiFinishedTurn=unit[32]
        new_unit.applyRaceModifiers()
        new_unit.applyEquipmentModifiers()
        new_unit.getParentCell()
        new_unit.player=0
        new_unit.getCenter(new_unit.x, new_unit.y)
        #new_unit.getRect(new_unit.x, new_unit.y)
        new_unit.createMask()
        Main.players[0].units.append(new_unit)
    
    for unit in data['players'][1]['units']:
        new_unit=Unit(False,1,'','human')
        new_unit.id=unit[0]
        new_unit.nome=unit[1]
        new_unit.x=unit[2]
        new_unit.y=unit[3]
        new_unit.col=unit[4]
        new_unit.row=unit[5]
        new_unit.center=unit[6]
        new_unit.animated=unit[7]
        new_unit.flipChecker=unit[8]
        new_unit.atkOpportunityCheck=unit[17]
        new_unit.ai=unit[18]
        new_unit.inventory=unit[19]
        new_unit.activated=unit[20]
        new_unit.selected=unit[21]
        new_unit.moving=unit[23]
        new_unit.moved=unit[24]
        new_unit.race=unit[30]
        new_unit.basestats=unit[31]
        new_unit.aiFinishedTurn=unit[32]
        new_unit.applyRaceModifiers()
        new_unit.applyEquipmentModifiers()
        new_unit.getParentCell()
        new_unit.player=1
        new_unit.getCenter(new_unit.x, new_unit.y)
        #new_unit.getRect(new_unit.x, new_unit.y)
        
        new_unit.flipImage()
        new_unit.createMask()
        new_unit.hp=unit[9]
        
        Main.players[1].units.append(new_unit)

    print(Main.players[0].units)
    Main.room.roomNumber=2