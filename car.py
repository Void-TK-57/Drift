import pygame
import numpy as np 
from graphics import Scale, Slide, Rotate, transform


# car class
class Car:

    def __init__(self, x, y, width, height, velocity, angle_velocity, angle = 0, color = (255, 153, 187)):
        self.angle = angle

        self.x = x
        self.y = y
        self.height = height
        self.width = width

        self.vel = np.array([0, 0])
        self.angle_vel = 0

        self.p_vel = velocity
        self.p_angle_vel = angle_velocity

        self.color = color

    # draw the rectangle
    def draw(self, screen):
        coords =  [ [self.x - self.width, self.y - self.height], 
                    [self.x - self.width, self.y + self.height], 
                    [self.x + self.width, self.y + self.height],
                    [self.x + self.width, self.y - self.height] ]
        # rotate
        coords = np.array(coords)
        # transformations
        transformations = [Slide(-self.x, -self.y), Rotate(self.angle*np.pi), Slide(self.x, self.y)]
        #transformations = [Rotate(self.angle*np.pi), ]
        # new coords
        new_coords = transform(transformations, coords.T).T
        print(new_coords)
        for i in range(len(new_coords)):

            # draw the recangle
            pygame.draw.line(screen, self.color,  new_coords[i % len(new_coords)], new_coords[ (i + 1) % len(new_coords)] )
        #pygame.draw.polygon(screen, self.color,  new_coords )
        # calculate y and x of vertices
        x = self.x + np.sin(self.angle*np.pi)*250
        y = self.y - np.cos(self.angle*np.pi)*250
        # draw orientation
        pygame.draw.line(screen, (255, 255, 255), [self.x, self.y], [x, y] )

    
    # polar to cartesian
    def polar_to_cartesian(self, angle, magnitude):
        x = magnitude*np.sin( angle*np.pi )
        y = -magnitude*np.cos( angle*np.pi )
        return x, y

    def move(self, directions):
        # coefficients of up, right, left and down
        magnitude = 0 - directions[0] + directions[2]
        angle = 0 + directions[1] - directions[3]
        #self.velocity = self.polar_to_cartesian(self.angle + angle*self.fixed_angular_velocity, magnitude*self.fixed_velocity)
        self.vel = self.polar_to_cartesian(self.angle+1, magnitude*self.p_vel)
        self.angle_vel = angle*self.p_angle_vel

    def rotate(self, anti = False):
        angular_velocity = self.fixed_angular_velocity
        if anti:
            angular_velocity *= -1
        self.body.velocity = self.polar_to_cartesian(self.body.angle + angular_velocity, self.fixed_velocity)


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
