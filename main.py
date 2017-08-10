import pygame
from pygame.locals import *
from constants import *
from classes import *
import time
###CONSTANTS###


###FUNCTIONS###

###TESTS###
if __name__=="__main__":
    #init
    pygame.init()

    #root surface
    root=pygame.display.set_mode( (root_width, root_height) )

    #classes
    objects=Objects(root)
    collision=Collision(objects)
    movement=Movement(objects, collision)
    animation=Animation(objects)

    #background
    background=pygame.Surface( (root_width, root_height) )
    background.fill((230,230,230))
    objects.add(background, 0 ,0, "background")

    #character
    character=pygame.Surface( (50,100) )
    character.fill((255,128,0))
    objects.add(character, root_width//2, root_height//2, "character")
    collision.add("character")

    #wall
    wall=pygame.Surface( (70,70) )
    wall.fill((0,128,255))
    objects.add(wall, root_width//2-100, root_height//2, "wall")
    movement.add("wall")
    #animation
    #key repeat
    pygame.key.set_repeat(1,16)

    #variables
    position="game"
    loop_principal=True
    a = 0

    while loop_principal:
        while position=="game":
            pygame.time.Clock().tick(timer_clock)

            animation.find()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    movement.processing(event.key)

                if event.type == MOUSEBUTTONDOWN:
                    if event.button==1:
                        if a == 0:
                            animation.start("nature/herbe", 100, 100, 3000, 2, "nature")
                            a = 1
                        else:
                            animation.start("nature/herbe", 200, 200, 3000, 2, "nature")
                    elif event.button==3:
                        animation.move("nature", 8, 8)

                if event.type == QUIT:
                    loop_principal = False
                    position="none"


            objects.display()

pygame.quit()
