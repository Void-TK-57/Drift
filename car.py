import pygame
import numpy as np 
import pymunk 


# car class
class Car:

    def __init__(self, x, y, width, height, velocity, color = (255, 153, 187)):
        # create body
        self.body = pymunk.Body(mass = 10, moment = 1)
        self.body.position = x, y
        self.shape = pymunk.Poly(self.body, [[0, 0], [0, height], [width, 0], [width, height] ] )
        self.fixed_velocity = velocity
        self.color = color

    # draw the rectangle
    def draw(self, screen):
        l = []

        for coord in  self.shape.get_vertices():
            print(coord)
            print(self.body.local_to_world(coord))
            l.append( self.body.local_to_world(coord) )
        print("---------")
        pygame.draw.polygon(screen, self.color,  l)
        

    # update velocity
    def update(self):
        pass
    #self.body.update_velocity(self.fixed_velocity)
