import pygame
from graphics import *

class Map:

    def __init__(self, lines):
        self.lines = lines
        self.colisions = []

    def draw(self, screen):
        # for each line
        for line in self.lines:
            pygame.draw.line(screen, line[1], [line[0].point1.x, line[0].point1.y ] , [line[0].point2.x, line[0].point2.y ] )

    def colision(self, car):
        # check detection for each line of map and vision
        for line in lines:
            for vision in car.visions:
                intersect = intersection(line, vision)
                if intersect is not None:
                    self.colisions.apend(intersect)
        
