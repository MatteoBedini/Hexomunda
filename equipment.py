import pygame
import os

def load(img):
    return pygame.image.load(img)
#template [hp,atk,move,atkpts,atkrange,cost,img,animation]
def loadAnimation(image_folder,images_partial_name,images_number,twohanded=False,current_frame=0,animation_speed=0.2,elapsed_time=0):

    
    animation_images = []
    for i in range(1,images_number+1):
        
        animation_images.append(pygame.image.load(os.path.join(image_folder, f"{images_partial_name}_{i}.png")))
        
    
    full_array=[]
    full_array.append(animation_images)
    full_array.append(twohanded)
    full_array.append(current_frame)
    full_array.append(animation_speed)
    full_array.append(elapsed_time)

    
    return full_array
    
def loadVariousAnimation(image_folder,images_partial_name,images_number,current_frame=0,animation_speed=0.2,elapsed_time=0):

    
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
                'goblin hood 1': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_hood_0.png'),('./media/races/goblin/animations/','goblin_base_hood_0',4)],
                'goblin hood 2': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_hood_1.png'),('./media/races/goblin/animations/','goblin_base_hood_1',4)],
                'goblin boss hood': [2,0,0,0,0,4,load('./media/races/goblin/goblin_boss_hood_0.png'),('./media/races/goblin/animations/','goblin_boss_hood_0',4)],
                'goblin cap': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_cap_0.png'),('./media/races/goblin/animations/','goblin_base_cap_0',4)],
                #humans
                'human plumed leather helmet': [1,0,0,0,0,2,load('./media/races/human/human_plumed_helmet_0.png'),('./media/races/human/animations/','human_plumed_helmet_0',4)],
                'human half steel helmet': [1,0,0,0,0,2,load('./media/races/human/human_steel_half_helmet_0.png'),('./media/races/human/animations/','human_steel_half_helmet_0',4)],
                'human full steel helmet': [2,0,0,0,0,4,load('./media/races/human/human_steel_full_helm_0.png'),('./media/races/human/animations/','human_steel_full_helm_0',4)],
                'human leather helmet': [2,0,0,0,0,4,load('./media/races/human/human_plumed_leather_helmet_0.png'),('./media/races/human/animations/','human_plumed_leather_helmet_0',4)],
                'human half steel helmet 1': [1,0,0,0,0,2,load('./media/races/human/human_steel_half_helmet_1.png'),('./media/races/human/animations/','human_steel_half_helmet_1',4)],
                #orcs
                'orc full steel helm 1': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_0.png'),('./media/races/orc/animations/','orc_steel_full_helm_0',4)],
                'orc full steel helm 2': [1,0,0,0,0,2,load('./media/races/orc/orc_steel_full_helm_1.png'),('./media/races/orc/animations/','orc_steel_full_helm_1',4)],
                #dwarves
                'dwarf helmet 1': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_winged_helmet_0.png'),('./media/races/dwarf/animations/','dwarf_winged_helmet_0',4)],
                'dwarf lord helm': [2,0,0,0,0,4,load('./media/races/dwarf/dwarf_lord_horned_helm_0.png'),('./media/races/dwarf/animations/','dwarf_lord_horned_helm_0',4)],
                'dwarf helmet 0': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_base_helm_0.png'),('./media/races/dwarf/animations/','dwarf_base_helm_0',4)],

}

all['body']={   #goblins
                'goblin base robe': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_robe_0.png'),('./media/races/goblin/animations/','goblin_base_robe_0',4)],
                'goblin leather armor': [1,0,0,0,0,2,load('./media/races/goblin/goblin_leather_armor_0.png'),('./media/races/goblin/animations/','goblin_leather_armor_0',4)],
                #humans
                'human steel half armor 1': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_1.png'),('./media/races/human/animations/','human_base_armor_1',4)],
                'human steel half armor 0': [2,0,0,0,0,3,load('./media/races/human/human_base_armor_0.png'),('./media/races/human/animations/','human_base_armor_0',4)],
                'human full steel armor': [3,0,0,0,0,5,load('./media/races/human/human_steel_full_armor_0.png'),('./media/races/human/animations/','human_steel_full_armor_0',4)],
                #orcs
                'orc steel full armor': [3,0,0,0,0,5,load('./media/races/orc/orc_steel_full_armor_0.png'),('./media/races/orc/animations/','orc_steel_full_armor_0',4)],
                #dwarves
                'dwarf steel full armor': [3,0,0,0,0,5,load('./media/races/dwarf/dwarf_lord_armor_0.png'),('./media/races/dwarf/animations/','dwarf_lord_armor_0',4)],
                'dwarf base armor': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_base_armor_0.png'),('./media/races/dwarf/animations/','dwarf_base_armor_0',4)],

}

all['rhand']={  #goblins
                'goblin moon shield': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_shield_0.png'),('./media/races/goblin/animations/','goblin_base_shield_0',4)],
                'goblin spear': [0,1,0,0,0,8,load('./media/races/goblin/goblin_pike_0.png'),('./media/races/goblin/animations/','goblin_pike_0',4,True)],
                'goblin leather shield': [1,0,0,0,0,2,load('./media/races/goblin/goblin_base_shield_1.png'),('./media/races/goblin/animations/','goblin_base_shield_1',4)],
                #humans
                'human shield': [1,0,0,0,0,2,load('./media/races/human/human_base_shield_0.png'),('./media/races/human/animations/','human_base_shield_0',4)],
                'human crossbow':[0,1,0,0,2,8,load('./media/races/human/human_crossbow_0.png'),('./media/races/human/animations/','human_crossbow_0',4,True)],
                'human halberd':[0,2,0,0,0,6,load('./media/races/human/human_halberd_0.png'),('./media/races/human/animations/','human_halberd_0',4,True)],
                #orcs
                'orc shield': [1,0,0,0,0,2,load('./media/races/orc/orc_base_shield_0.png'),('./media/races/orc/animations/','orc_base_shield_0',4)],
                #dwarves
                'dwarf shield': [1,0,0,0,0,2,load('./media/races/dwarf/dwarf_blue_shield_0.png'),('./media/races/dwarf/animations/','dwarf_blue_shield_0',4)],


                
               }

all['lhand']={  #goblins
                'goblin sword':[0,1,0,0,0,2,load('./media/races/goblin/goblin_base_sword_0.png'),('./media/races/goblin/animations/','goblin_base_sword_0',4)],
                'goblin shortbow':[0,0,0,0,2,6,load('./media/races/goblin/goblin_bow_0.png'),('./media/races/goblin/animations/','goblin_bow_0',4,True)],
                #humans
                'human sword':[0,1,0,0,0,2,load('./media/races/human/human_base_sword_0.png'),('./media/races/human/animations/','human_base_sword_0',4)],
                #orcs
                'orc sword':[0,1,0,0,0,2,load('./media/races/orc/orc_base_sword_0.png'),('./media/races/orc/animations/','orc_base_sword_0',4)],
                
                'orc 2h axe':[0,2,0,0,0,6,load('./media/races/orc/orc_two_handed_axe_0.png'),('./media/races/orc/animations/','orc_two_handed_axe_0',4,True)],
                #dwarves
                'dwarf axe':[0,1,0,0,0,2,load('./media/races/dwarf/dwarf_axe_0.png'),('./media/races/dwarf/animations/','dwarf_axe_0',4)],
                'dwarf 2h axe':[0,2,0,0,0,6,load('./media/races/dwarf/dwarf_2h_axe_0.png'),('./media/races/dwarf/animations/','dwarf_2h_axe_0',4,True)],
               
               }



#various animations
atk_animation=loadAnimation('./media/various_anims/','attack',7,animation_speed=0.05)
ranged_atk_animation=loadAnimation('./media/various_anims/','ranged',7,animation_speed=0.05)