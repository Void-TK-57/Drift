import numpy as np

class Rotate():
    def __init__(self, angle):
        self.angle = angle

    def __call__(self, coords):
        matrix=np.array([[np.cos(self.angle), -np.sin(self.angle), 0],
                    [ np.sin(self.angle),  np.cos(self.angle), 0],
                    [      0       ,         0     , 1]])
        return matrix @ coords

class Scale():
    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy

    def __call__(self, coords):
        matrix=np.array([[self.sx, 0, 0],
                    [ 0, self.sy, 0],
                    [ 0,  0, 1 ]])
        return matrix @ coords


class Slide():
    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def __call__(self, coords):
        matrix=np.array([[1, 0, self.tx],
                    [ 0, 1, self.ty],
                    [ 0, 0, 1 ]])
        return matrix @ coords 

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Line(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Line(self.x - other.x, self.y - other.y)

    def __iter__(self):
        self._end = False
        return self.x

    def __next__(self):
        if(self._end):
            raise StopIteration
        else:
            self._end = True
            return self.y

class Line:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __len__(self):
        return ( (self.point1.x - self.point2.x)**2 + (self.point1.y - self.point2.y)**2 )**0.5

    def __add__(self, other):
        return Line(self.point1 + other.point1, self.point2 + other.point2)

    def __sub__(self, other):
        return Line(self.point1 - other.point1, self.point2 - other.point2)

    def intersection(self, other):
        x1 = self.point1.x
        y1 = self.point1.y
        x2 = self.point2.x
        y2 = self.point2.y
        x3 = other.point1.x
        y3 = other.point1.y
        x4 = other.point2.x
        y4 = other.point2.y

        x = ( (x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4) ) / (x1-x2)(y3-y4) - (y1-y2)(x3-x4)
        y = ( (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4) ) / (x1-x2)(y3-y4) - (y1-y2)(x3-x4)

        return Point(x, y)

    def __iter__(self):
        self._end = False
        return self.point1

    def __next__(self):
        if(self._end):
            raise StopIteration
        else:
            self._end = True
            return self.point2


def homogen(matrix):
    return np.concatenate( [matrix, np.ones( [1, matrix.shape[1]] ) ], axis = 0)

def de_homogen(matrix):
    return matrix[:-1, :]

def transform(transforms, matrix):
    homogen_matrix = homogen(matrix)
    for func in transforms:
        homogen_matrix = func(homogen_matrix)
    return de_homogen(homogen_matrix)

if __name__ == "__main__":
    a = np.array([[0, 4], [1, 2]])
    print(a)
    b = transform( [Slide(2, 2), Scale(3, 2), Slide(1, -1)], a )
    print(b)