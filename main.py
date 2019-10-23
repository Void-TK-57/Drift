import pygame
from pygame.locals import *
import numpy as np
from car import Car
from maplib import Map
from graphics import *


def update_game(screen, car, _map, dt, directions):
    # update velocity and angular velocity
    car.move(directions)
    # update car position and box coordinates
    car.update()
    # check car vision collisions
    car.colision()

    # reset screen and redraw
    screen.fill((0, 0, 0))
    car.draw(screen)
    _map.draw(screen)
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
    
    _map = Map( [ Line( Point(870, 40), Point(540, 310) ) ] )
    
    car = Car(x = 200, y = 200, width = 7, height = 16, _map = _map, velocity = 5, angle_velocity=0.02, angle = 0)

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
    
        # update game and tick clock
        update_game(screen, car, _map, clock.get_time(), key_pressed)
        clock.tick(60)

        car.log()
        
    
    # quit
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()