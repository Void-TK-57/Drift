import pygame
from pygame.locals import *
import numpy as np
from car import Car


import pymunk

def update_game(screen, space, car, _map, dt):
    # update worlrd
    space.step(dt/1000)
    #car.body.torque = 4
    print( car.body.position )
    print( car.body.angle)
    # reset screen and redraw
    screen.fill((0, 0, 0))
    car.draw(screen)
    # update display
    pygame.display.update()

def main():

    pygame.init()

    # display height and width
    display_height = 600
    disply_width = 1000

    screen = pygame.display.set_mode( (disply_width, display_height) )
    pygame.display.set_caption('Race Drift')

    clock = pygame.time.Clock()
    # check if the game is still alive
    alive = True

    _map = []
    
    space = pymunk.Space()
    space.gravity = 0, 0

    car = Car(x = 200, y = 200, width = 14, height = 32, velocity = 10)

    space.add(car.body, car.shape)

    
    # main loop
    while alive:
        # for each event
        for event in pygame.event.get():
            # if event is quit, then set alive to false
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # add for at the bottom of the car
                    print("Up")
                    
                elif event.key == pygame.K_UP:
                    print("Down")

    
        # update game and tick clock
        update_game(screen, space, car, _map, clock.get_time())
        clock.tick(60)
        
    
    # quit
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()