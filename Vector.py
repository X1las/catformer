# Imports
import math, copy

# Vector class
class Vec(object):

    # Class Variables
    __slots__=['x', 'y', 'len', 'mag']

    # Initializer
    def __init__(self, x=0, y=0):
        self.x = x; self.y = y


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__getattribute__(self.__slots__[item])
        if isinstance(item, str):
            return self.__getattribute__(item)


    def __setitem__(self, item, insert):
        if isinstance(item, int):
            self.__setattr__(self.__slots__[item], insert)
        if isinstance(item, str):
            self.__setattr__(item, insert)

    # Method for adding two vectors
    def __add__(self, other):
        newx = self.x + other.x; newy = self.y + other.y
        return Vec(newx, newy)

    # Method for subtracting two vectors
    def __sub__(self, other):
        newx = self.x - other.x; newy = self.y - other.y
        return Vec(newx, newy)

    # Method for multiplying a vector by a scalar
    def __mul__(self, scale : (float or int)):
        newx = self.x * scale; newy = self.y * scale
        return Vec(newx, newy)

    # Method for dividing a vector by a scalar
    def __truediv__(self, scale : (float or int)):
        newx = self.x / scale; newy = self.y / scale
        return Vec(newx, newy)

    # Method for calculating the length/magnitude of a vector
    def length(self):
        self.len = math.sqrt(self.x**2+self.y**2)
        return self.len
    
    # Returns a string representation of the vector: (x,y)
    def __str__(self):
        return f'({self.x},{self.y})'

    # Returns the vector in absolute values
    def __abs__(self):
        newx = abs(self.x)
        newy = abs(self.y)
        return Vec(newx, newy)

    # Returns the vector as a list
    def setList(self, x, y):
        self.lis = [x,y]

    # Return the vector as a tuple
    def asTuple(self):
        return (self.x,self.y)

    # Method for rounding the vector (half away from zero)
    def rounded(self):
        roundedx = self.normRound(self.x)
        roundedy = self.normRound(self.y)
        return Vec(roundedx,roundedy)

    # Method for rounding a number (half away from zero)
    def normRound(self, number):
        neg = False
        if number < 0:
            neg = True
        inte = math.floor(number)
        dec = number - inte
        if dec*10 >= 5 and not neg or dec*10 > 5 and neg:
            result = 1
        else:
            result = 0
        return inte + result    

    def printExact(self):
        print(f'({self.x},{self.y})')

    def copy(self):
        return Vec(copy.copy(self.x),copy.copy(self.y))


