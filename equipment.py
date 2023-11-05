import pygame

def load(img):
    return pygame.image.load(img)
#template [hp,atk,move,atkpts,atkrange,cost,img]
all={}

all['head']={   #goblins
                'goblin hood 1': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_hood_0.png')],
                'goblin boss hood': [2,0,0,0,0,4,load('./media/races/goblin/goblin_boss_hood_0.png')],
                #humans
                'human plumed leather helmet': [1,0,0,0,0,2,load('./media/races/human/human_plumed_helmet_0.png')],
                'human half steel helmet': [1,0,0,0,0,2,load('./media/races/human/human_steel_half_helmet_0.png')],
                'human full steel helmet': [2,0,0,0,0,4,load('./media/races/human/human_steel_full_helm_0.png')],
                'human leather helmet': [2,0,0,0,0,4,load('./media/races/human/human_plumed_leather_helmet_0.png')],
                #orcs
                'orc ful steel helm 1': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_0.png')],
                'orc ful steel helm 2': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_1.png')],

}

all['body']={   #goblins
                'goblin base robe': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_robe_0.png')],
                #humans
                'human steel half armor 1': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_1.png')],
                'human steel half armor 0': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_0.png')],
                'human full steel armor': [3,0,0,0,0,5,load('./media/races/human/human_steel_full_armor_0.png')],
                #orcs
                'orc steel full armor': [3,0,0,0,0,5,load('./media/races/orc/orc_steel_full_armor_0.png')],

}

all['rhand']={  #goblins
                'goblin shield': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_shield_0.png')],
                #humans
                'human shield': [1,0,0,0,0,2,load('./media/races/human/human_base_shield_0.png')],
                #orcs
                'orc shield': [1,0,0,0,0,2,load('./media/races/orc/orc_base_shield_0.png')],
                
               }

all['lhand']={  #goblins
                'goblin sword':[0,1,0,0,0,2,load('./media/races/goblin/goblin_base_sword_0.png')],
                #humans
                'human sword':[0,1,0,0,0,2,load('./media/races/human/human_base_sword_0.png')],
                #orcs
                'orc sword':[0,1,0,0,0,2,load('./media/races/orc/orc_base_sword_0.png')],
                'orc 2h axe':[0,2,0,0,0,4,load('./media/races/orc/orc_two_handed_axe_0.png')],
               
               }


