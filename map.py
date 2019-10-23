import pygame
from graphics import *

class Map:

    def __init__(self, lines):
        self.lines = lines

    def draw(self, screen):
        # for each line
        for line in self.lines:
            pygame.draw.line(screen, line[1], [line[0].point1.x, line[0].point1.y ] , [line[0].point2.x, line[0].point2.y ] )

        
