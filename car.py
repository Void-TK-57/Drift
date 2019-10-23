import pygame
import numpy as np 
import pymunk 
from pymunk.vec2d import Vec2d


# car class
class Car:

    def __init__(self, x, y, width, height, velocity, angular_velocity, color = (255, 153, 187)):
        # create body
        self.body = pymunk.Body(mass = 0, moment = 0, body_type= pymunk.Body.DYNAMIC)
        self.body.position = x, y
        #self.shape = pymunk.Poly(self.body, [[0, 0], [0, height], [width, 0], [width, height] ] )
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.mass = 0.001
        self.shape.density = 1
        self.fixed_velocity = velocity
        self.color = color
        self.height = height
        self.width = width
        self.fixed_angular_velocity = angular_velocity

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
        pygame.draw.line(screen, (255, 255, 255), list(self.body.position), self.body.local_to_world( [100*np.sin(self.body.angle/180) , -100*np.cos(self.body.angle/180)] ) )

    # method to get the local point of the vector
    def get_point_from_wheel(self, wheel):
        wheels = wheel.split("-")
        if wheels[0] == "bottom":
            y_orientation = -1
        elif wheels[0] == "top":
            y_orientation = 1
        else:
            y_orientation = 0
        
        if wheels[0] == "left":
            x_orientation = -1
        elif wheels[0] == "right":
            x_orientation = 1
        else:
            x_orientation = 0

        y = y_orientation * self.height/2
        x = x_orientation * self.width/2
        return x, y

    def polar_to_cartesian(self, angle, length):
        return [length * np.cos(angle + np.pi/2), -length * np.sin(angle + np.pi/2)]

    def apply_force_at_local_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, self.get_point_from_wheel(wheel) )

    def apply_force_at_world_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, self.get_point_from_wheel(wheel) )

    def apply_impulse_at_local_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, self.get_point_from_wheel(wheel) )

    def apply_impulse_at_world_point(self, force, wheel):
        self.body.apply_force_at_local_point(force, self.get_point_from_wheel(wheel) )

    def move(self, backwards = False):
        velocity = self.fixed_velocity
        if backwards:
            velocity *= -1
        self.body.velocity = self.polar_to_cartesian(-self.body.angle, velocity)

    def rotate(self, anti = False):
        angular_velocity = self.fixed_angular_velocity
        if anti:
            angular_velocity *= -1
        self.body.angular_velocity = angular_velocity

    def stop(self, rotation = False):
        if rotation:
            self.body.angular_velocity = 0
        else:
            self.body.velocity = 0, 0

    

    def log(self):
        print("Position:")
        print(self.body.position)
        print("Velocity:")
        print(self.body.velocity)
        print("Force:")
        print(self.body.force)
        print("-"*5)
        print("Angle:")
        print(self.body.angle/np.pi % 2)
        print("Angular Velocity:")
        print(self.body.angular_velocity)
        print("Torque:")
        print(self.body.torque)
        print("="*20)

    # update velocity
    def update(self):
        pass
    #self.body.update_velocity(self.fixed_velocity)
