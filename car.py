import pygame
import numpy as np 
from graphics import *
import Vector2D as vec


# car class (255, 153, 187)
class Car:

    def __init__(self, x, y, width, height, velocity, drift, acc, _map, max_drift, angle = 0, n_visions = 8, length_vision = 200, color = (0, 250, 0) ):
        # paramters of the bounding box
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.coords = np.array([[self.x - self.width, self.y - self.height], 
                                [self.x - self.width, self.y + self.height], 
                                [self.x + self.width, self.y + self.height],
                                [self.x + self.width, self.y - self.height] ] )

        # angle velocity (which is the angle of car - the drift)
        self.angle = angle
        # actual velocity, and reference velocity
        self.vel = np.array([0, 0])
        self.p_vel = velocity
        
        # drift
        self.drift_angle = 0
        self.max_drift = max_drift
        # variation of the drift
        self.drift = drift
        # variation of angle velocity
        self.acc = acc

        # draw parameters
        self.color = color
        self._map = _map
        self.colision_color = (255, 255, 70)

        # vision parameter
        self.colisions = []
        self.n_visions = n_visions
        self.length_vision = length_vision
        self.visions = self.get_visions(n_visions, length_vision)

        self.crash = False

    # update position, angle, and bounding box coordinates and visions coordinates
    def update(self, directions, dt):
        # coefficient if its goint to up or down, and right or left
        magnitude = 0 + directions[0] - directions[2]
        angle = 0 + directions[1] - directions[3]
        
        # change angle based on acceleration
        self.angle += self.acc*dt*angle
        self.angle %= 2
        
        # set velocity based on angle
        self.vel[0] = self.p_vel*np.sin(self.angle*np.pi)
        self.vel[1] = self.p_vel*np.cos(self.angle*np.pi)
        # change position
        self.x += self.vel[0]*dt*magnitude
        self.y -= self.vel[1]*dt*magnitude
        
        # check direction for drift
        if directions[1]:
            drift_coef = 1
        elif directions[3]:
            drift_coef = -1
        elif self.drift_angle > 0.01:
            drift_coef = -1.5 # restitution is 1.5 of the drift
        elif self.drift_angle < -0.01:
            drift_coef = 1.5 # restitution is 1.5 of the drift
        else:
            drift_coef = 0
        
        # drift variation
        d_drift = self.drift*dt
        self.drift_angle += drift_coef*d_drift*abs(magnitude)
        # ceil
        if abs(self.drift_angle) > self.max_drift:
            self.drift_angle = self.max_drift*(self.drift_angle)/abs(self.drift_angle)

        # coords of the bounding box
        coords = np.array( [[self.x - self.width, self.y - self.height], 
                            [self.x - self.width, self.y + self.height], 
                            [self.x + self.width, self.y + self.height],
                            [self.x + self.width, self.y - self.height] ] )
        
        # update car box coordinates by transformating by rorating by car angle + drift angle
        transformations = [Slide(-self.x, -self.y), Rotate((self.angle+self.drift_angle)*np.pi), Slide(self.x, self.y)]
        # new coords rotated on the point x, y
        self.coords = transform(transformations, coords.T).T

        # update visions
        self.visions = self.get_visions(self.n_visions, self.length_vision)

    # function to get line visions based on the number of visions and length of line
    def get_visions(self, n, length):
        visions = []
        for i in range(n):
            x = self.x + np.sin( i*(2*np.pi/n) + (self.angle+self.drift_angle)*np.pi)*length
            y = self.y - np.cos( i*(2*np.pi/n) + (self.angle+self.drift_angle)*np.pi)*length
            visions.append (Line( Point(self.x, self.y), Point( x, y) ) )
        return visions
        
    # draw the bounding box and visions
    def draw(self, screen, velocity = True, enable_visions = False):
        # Draw Polygon

        #pygame.draw.polygon(screen, (0, 0, 0) , self.coords )
        
        if velocity:
            pygame.draw.line(screen, (0, 0, 255), [self.x, self.y], [self.x + self.vel[0], self.y - self.vel[1]] )
        
        if enable_visions:
            # draw visions
            for vision in self.visions:
                pygame.draw.line(screen, (255, 255, 255), [vision.point1.x, vision.point1.y], [vision.point2.x, vision.point2.y] )
            # for each collisions
            for collision in self.colisions:
                pygame.draw.circle(screen, (255, 0, 0), [int(collision[0].x), int(collision[0].y)], 5)
        
        pygame.draw.polygon(screen, self.color if not self.crash else (255, 0, 0) , self.coords )
    
    # log values of the color
    def log(self):
        angle = lambda x, y: np.arctan2(x, y)
        abs_ = lambda x, y: (x**2 + y**2)**0.5
        print("Position:")
        print(self.x, self.y)
        print("Velocity:")
        print(self.vel)
        print("Velocity Polar:")
        print(abs_(self.vel[0], self.vel[1]), angle(self.vel[0], self.vel[1])/np.pi)
        print("Angle:")
        print(self.angle)
        print("Drift Angle:")
        print(self.drift_angle)
        print("="*20)

    # check collision of visions and add points of the collisions to a list
    def colision(self):

        # check colission with the map
        self.crash = self._map.collision(self)

        # empty collision
        self.colisions = []
        # check detection for each line of map and vision
        for vision in self.visions:
            intersect_visions = []
            for line in self._map.lines:
                intersect = line.intersection(vision)
                if intersect is not None:
                    # get distance of intersect to the line
                    distance = Line( Point( (self.x), self.y), intersect).length()
                    intersect_visions.append( [ intersect, distance ] )

            # get intersect of minimum disance
            try:
                self.colisions.append( min(intersect_visions, key = lambda x : x[1]) )
            except Exception as err:
                pass


def load_car(data, _map):
    return Car(x = data["car"]["x"], y = data["car"]["y"], width = data["car"]["width"], height = data["car"]["height"], _map = _map, velocity = data["car"]["velocity"], acc=data["car"]["acc"], drift=data["car"]["drift"], max_drift=data["car"]["max_drift"], angle = data["car"]["angle"])

        
