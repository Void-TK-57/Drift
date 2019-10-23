import pygame
from pygame.locals import *
import numpy as np
from car import Car


import pymunk

def update_game(screen, space, car, _map, dt):
    # update worlrd
    space.step(dt/1000)
    # reset screen and redraw
    screen.fill((0, 0, 0))
    car.draw(screen)
    # update display
    pygame.display.update()

def main():
    # init game
    pygame.init()

    # display height and width
    display_height = 600
    disply_width = 800
    # UP, RIGHT, DOWN, LEFT
    key_pressed = [False, False, False, False]


    screen = pygame.display.set_mode( (disply_width, display_height) )
    pygame.display.set_caption('Race Drift')

    clock = pygame.time.Clock()
    _map = []
    
    space = pymunk.Space()
    space.gravity = 0, 0

    car = Car(x = 200, y = 200, width = 14, height = 32, velocity = 200, angular_velocity = 1.4)

    space.add(car.body, car.shape)

    # main loop
    while True:
        # for each event
        for event in pygame.event.get():
            # if event is quit, then set alive to false
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # change state of the key pressed
                if event.key ==pygame.K_UP:
                    key_pressed[0] = not key_pressed[0]
                if event.key ==pygame.K_RIGHT:
                    key_pressed[1] = not key_pressed[1]
                if event.key ==pygame.K_DOWN:
                    key_pressed[2] = not key_pressed[2]
                if event.key ==pygame.K_LEFT:
                    key_pressed[3] = not key_pressed[3]

        
        # if there is a key pressed, check which one
        if key_pressed[0]:
            car.move()
        if key_pressed[2]:
            car.move(backwards=True)
        if key_pressed[1]:
            car.rotate()
        if key_pressed[3]:
            car.rotate(anti = True)

        # if neither of keys are pressed, stop car
        if not ( key_pressed[0] or key_pressed[2] ):
            car.stop()
        if not ( key_pressed[1] or key_pressed[3] ):
            car.stop(True)
    
        # update game and tick clock
        update_game(screen, space, car, _map, clock.get_time())
        clock.tick(60)

        car.log()
        
    
    # quit
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()