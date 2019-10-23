import pygame
from pygame.locals import *
import numpy as np
from car import Car


def update_game(screen, car, _map, dt):
    car.update()
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
    
    car = Car(x = 200, y = 200, width = 14, height = 32, velocity = 10, angle_velocity=0.01, angle = 0)

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
        car.move(key_pressed)
    
        # update game and tick clock
        update_game(screen, car, _map, clock.get_time())
        clock.tick(60)

        car.log()
        
    
    # quit
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()