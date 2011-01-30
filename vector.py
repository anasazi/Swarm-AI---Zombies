#Alice Forehand
#Robert Pienta
#Eric Reed

from math import acos, sqrt, pi

class Vector:
    """A simple 2d vector

    >>> v1 = Vector(1,0)
    >>> v2 = Vector(0,1)
    >>> print(v1.add(v2))
    (1, 1)
    >>> print(v1 + v2)
    (1, 1)
    >>> print(v1.subtract(v2))
    (1, -1)
    >>> print(v1 - v2)
    (1, -1)
    >>> print(v1 / 2)
    (0.5, 0.0)
    >>> print(v1 * 3)
    (3, 0)
    >>> v1.magnitude()
    1.0
    >>> v2.magnitude()
    1.0
    >>> v1.dotProduct(v2)
    0
    >>> v2.dotProduct(v1)
    0
    >>> v1.dotProduct(v1)
    1
    >>> v2.dotProduct(v2)
    1
    >>> print(v1)
    (1, 0)
    >>> v1.angleBetween(v2)*180/pi
    90.0
    >>> print(v1.projection(v2))
    (0.0, 0.0)
    >>> print(v1.truncate(.5))
    (0.5, 0.0)
    >>> v3 = Vector(1,1)
    >>> print(v3.truncate(1))
    (0.707106781187, 0.707106781187)
    """
    def __init__(self, xi, yi):
        self.x = xi
        self.y = yi
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
    def add(self, v1):
        return Vector(self.x+v1.x, self.y+v1.y)
    def __add__(self, v1):
        return Vector(self.x+v1.x, self.y+v1.y)
    def subtract(self, v1):
        return Vector(self.x-v1.x, self.y-v1.y)
    def __sub__(self, v1):
        return Vector(self.x-v1.x, self.y-v1.y)
    def __truediv__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar)
    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    def scalarMult(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    def magnitude(self):
        return sqrt(self.x*self.x + self.y*self.y)
    def magnitudeSansRoot(self):
        return self.x*self.x + self.y*self.y
    def dotProduct(self, v1):
        return self.x*v1.x + self.y*v1.y
    def angleBetween(self, v1):
        return acos(self.dotProduct(v1)/(self.magnitude()*v1.magnitude()))
    def projection(self, v1):
        return v1.scalarMult(self.dotProduct(v1)/v1.magnitudeSansRoot())
    def truncate(self, scalar):
        mag = self.magnitude()
        if(mag > scalar):
           return Vector(self.x/mag*scalar, self.y/mag*scalar)
        return Vector(self.x, self.y) 
    def vec2tuple(self):
        return (self.x, self.y)
       


        
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

        
        
