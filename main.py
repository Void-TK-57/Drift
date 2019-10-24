import pygame
from pygame.locals import *
import numpy as np
from car import Car, load_car
from maplib import Map, load_map
from graphics import *
import json

import sys


def update_game(screen, car, _map, dt, directions):
    
    # update car position and box coordinates
    car.update(directions, dt)
    # check car vision collisions
    car.colision()

    # reset screen and redraw
    screen.fill((65, 65, 65))
    car.draw(screen)
    _map.draw(screen)
    # update display
    pygame.display.update()

def main(map_path):
    # read json
    with open(map_path) as json_file:
        data = json.load(json_file)
    # init game
    pygame.init()

    # display height and width
    display_height = 500
    disply_width = 800
    # UP, RIGHT, DOWN, LEFT
    key_pressed = [False, False, False, False]


    screen = pygame.display.set_mode( (disply_width, display_height) )
    pygame.display.set_caption('Race Drift')

    clock = pygame.time.Clock()
    
    _map = load_map(data)
    
    car = load_car(data, _map)

    # main loop
    while True:
        # for each event
        for event in pygame.event.get():
            # if event is quit, then set alive to false
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
        update_game(screen, car, _map, clock.get_time()/1000.0, key_pressed)
        clock.tick(30)

        car.log()

if __name__ == "__main__":
    main(sys.argv[1])