import numpy as np

class Rotate():
    def __init__(self, angle):
        self.angle = angle

    def __call__(self, coords):
        matrix=np.array([[np.cos(self.angle), -np.sin(self.angle), 0],
                    [ np.cos(self.angle),  np.sin(self.angle), 0],
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