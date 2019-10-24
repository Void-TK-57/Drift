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
        lines = []
        n_points = car.coords.shape[0]
        # treat car as 4 lines
        for index_coords in range(n_points ):
           lines.append( Line(  Point( car.coords[index_coords][0]                , car.coords[index_coords][1]                 ),
                                Point( car.coords[( index_coords + 1)%n_points][0], car.coords[( index_coords + 1)%n_points][1] )   )   )
        # check collision for each line
        for line in self.lines:
            for car_line in lines:
                point = line.intersection(car_line)
                # if there is a point of collision, return true
                if point is not None:
                    return True

        
def load_map(data, color = (255, 255, 255)):
    points = {}
    lines = []
    # for each creates points
    for side in data.keys():
        if side == "car":
            continue
        points[side] = []
        # for each line
        for point in data[side]:
            points[side].append( Point(point[0], point[1]) )

    # for each point, create lines
    for side in points.keys():
        if side == "car":
            continue
        size = len( data[side] )
        # for each line
        for point_index in range( size ):
            lines.append( Line( points[side][point_index]  , points[side][ (point_index+1) % size ] ) )

    return Map(lines, color)
    



        
