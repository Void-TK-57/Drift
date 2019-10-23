import pygame
from graphics import *

class Map:

    def __init__(self, lines, color = (255, 255, 255)):
        self.lines = lines
        self.color = color

    # method to draw the line of the map
    def draw(self, screen, collisions = True):
        # for each line
        for line in self.lines:
            pygame.draw.line(screen, self.color, [line.point1.x, line.point1.y ] , [line.point2.x, line.point2.y ] )

    # method to check the collision of a car on the map
    def collision(self, car):
        # treat car as 4 lines
        pass


        
