import pygame
import numpy as np 
from graphics import *


# car class
class Car:

    def __init__(self, x, y, width, height, velocity, angle_velocity, _map, angle = 0, n_visions = 8, length_vision = 200, color = (255, 153, 187)):
        self.angle = angle

        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.coords =  [[self.x - self.width, self.y - self.height], 
                        [self.x - self.width, self.y + self.height], 
                        [self.x + self.width, self.y + self.height],
                        [self.x + self.width, self.y - self.height] ]
        

        self.vel = np.array([0, 0])
        self.angle_vel = 0

        self.p_vel = velocity
        self.p_angle_vel = angle_velocity

        self.color = color
        self.map = _map
        self.colision_color = (255, 255, 70)

        self.n_visions = n_visions
        self.length_vision = length_vision

        self.visions = self.get_visions(n_visions, length_vision)

    def get_visions(self, n, length):
        visions = []
        for i in range(n):
            x = self.x + np.sin( i*(2*np.pi/n) + self.angle*np.pi)*length
            y = self.y - np.cos( i*(2*np.pi/n) + self.angle*np.pi)*length
            visions.append (Line( Point(self.x, self.y), Point( x, y) ) )
        return visions
        
    # draw the rectangle
    def draw(self, screen, enable_visions = True):
        # Draw Polygon
        pygame.draw.polygon(screen, self.color, self.coords )
        
        if enable_visions:
            # draw visions
            for vision in self.visions:
                pygame.draw.line(screen, (255, 255, 255), [vision.point1.x, vision.point1.y], [vision.point2.x, vision.point2.y] )
    
    # polar to cartesian
    def polar_to_cartesian(self, angle, magnitude):
        x =  magnitude*np.sin( angle*np.pi )
        y = -magnitude*np.cos( angle*np.pi )
        return x, y

    def move(self, directions):
        magnitude = 0 - directions[0] + directions[2]
        angle = 0 + directions[1] - directions[3]
        
        self.vel = self.polar_to_cartesian(self.angle+1, magnitude*self.p_vel)
        self.angle_vel = angle*self.p_angle_vel

    def log(self):
        print("Position:")
        print(self.x, self.y)
        print("Velocity:")
        print(self.vel)
        print("Angle:")
        print(self.angle)
        print("Angle Velocity:")
        print(self.angle_vel)
        print("="*20)

    # update velocity
    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.angle += self.angle_vel
        self.angle %= 2.0
        # update car box coordinates
        # normal coordinates
        coords =  [ [self.x - self.width, self.y - self.height], 
                    [self.x - self.width, self.y + self.height], 
                    [self.x + self.width, self.y + self.height],
                    [self.x + self.width, self.y - self.height] ]
        # rotate the coordinates by angle
        coords = np.array(coords)
        # transformations for the rotations
        transformations = [Slide(-self.x, -self.y), Rotate(self.angle*np.pi), Slide(self.x, self.y)]
        # new coords rotated on the point x, y
        self.coords = transform(transformations, coords.T).T

        # update visions
        self.visions = self.get_visions(self.n_visions, self.length_vision)
        

    def collision(self):
        # treat car as 4 lines between the vertices
        pass
        
