import pygame
import numpy as np 
import pymunk 
from pymunk.vec2d import Vec2d


# car class
class Car:

    def __init__(self, x, y, width, height, velocity, color = (255, 153, 187)):
        # create body
        self.body = pymunk.Body(mass = 0, moment = 0, body_type= pymunk.Body.DYNAMIC)
        self.body.position = x, y
        #self.shape = pymunk.Poly(self.body, [[0, 0], [0, height], [width, 0], [width, height] ] )
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.mass = 1
        self.shape.density = 1
        self.fixed_velocity = velocity
        self.color = color

    # draw the rectangle
    def draw(self, screen):
        coords = []
        # conver to world
        for coord in  self.shape.get_vertices():
            coords.append( self.body.local_to_world(coord) )
        # draw the recangle
        pygame.draw.polygon(screen, self.color,  coords)
        # calculate y and x of vertices
        # draw orientation
        pygame.draw.line(screen, (255, 255, 255), list(self.body.position), self.body.local_to_world( [100*np.sin(self.body.angle) , -100*np.cos(self.body.angle)] ) )

    # method to get the local point of the vector
    def get_point_from_wheel(wheel):
        wheels = wheel.split("-")
        y_orientation = -1 if wheel[0] == "bottom" else 1
        x_orientation = -1 if wheel[1] == "right"  else 1
        y = y_orientation * self.shape.height/2
        x = x_orientation * self.shape.width/2
        return x, y

    def apply_force_at_local_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, wheel)

    def apply_force_at_world_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, wheel)

    def apply_impulse_at_local_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, wheel)

    def apply_impulse_at_world_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, wheel)
        

    # update velocity
    def update(self):
        pass
    #self.body.update_velocity(self.fixed_velocity)
