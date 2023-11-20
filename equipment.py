import pygame
import os

def load(img):
    return pygame.image.load(img)
#template [hp,atk,move,atkpts,atkrange,cost,img]
def loadAnimation(image_folder,images_partial_name,images_number,current_frame=0,animation_speed=0.2,elapsed_time=0):

    
    animation_images = []
    for i in range(1,images_number+1):
        
        animation_images.append(pygame.image.load(os.path.join(image_folder, f"{images_partial_name}_{i}.png")))
        
    
    full_array=[]
    full_array.append(animation_images)
    full_array.append(current_frame)
    full_array.append(animation_speed)
    full_array.append(elapsed_time)

    
    return full_array
    



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
                'orc full steel helm 1': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_0.png')],
                'orc full steel helm 2': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_1.png')],
                #dwarves
                'dwarf helmet 1': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_winged_helmet_0.png')],
                'dwarf lord helm': [2,0,0,0,0,4,load('./media/races/dwarf/dwarf_lord_horned_helm_0.png')],

}

all['body']={   #goblins
                'goblin base robe': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_robe_0.png')],
                #humans
                'human steel half armor 1': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_1.png')],
                'human steel half armor 0': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_0.png')],
                'human full steel armor': [3,0,0,0,0,5,load('./media/races/human/human_steel_full_armor_0.png')],
                #orcs
                'orc steel full armor': [3,0,0,0,0,5,load('./media/races/orc/orc_steel_full_armor_0.png')],
                #dwarves
                'dwarf steel full armor': [3,0,0,0,0,5,load('./media/races/dwarf/dwarf_lord_armor_0.png')],
                'dwarf base armor': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_base_armor_0.png')],

}

all['rhand']={  #goblins
                'goblin shield': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_shield_0.png')],
                #humans
                'human shield': [1,0,0,0,0,2,load('./media/races/human/human_base_shield_0.png')],
                #orcs
                'orc shield': [1,0,0,0,0,2,load('./media/races/orc/orc_base_shield_0.png')],
                #dwarves
                'dwarf shield': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_blue_shield_0.png')],
                
               }

all['lhand']={  #goblins
                'goblin sword':[0,1,0,0,0,2,load('./media/races/goblin/goblin_base_sword_0.png')],
                #humans
                'human sword':[0,1,0,0,0,2,load('./media/races/human/human_base_sword_0.png')],
                #orcs
                'orc sword':[0,1,0,0,0,2,load('./media/races/orc/orc_base_sword_0.png')],
                'orc 2h axe':[0,2,0,0,0,4,load('./media/races/orc/orc_two_handed_axe_0.png')],
                #dwarves
                'dwarf axe':[0,1,0,0,0,2,load('./media/races/dwarf/dwarf_axe_0.png')],
                'dwarf 2h axe':[0,2,0,0,0,4,load('./media/races/dwarf/dwarf_2h_axe_0.png')],
               
               }


