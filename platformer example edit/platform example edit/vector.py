import math
import copy



# (A part of) the Vec class:
class Vec(object):
    __slots__=['x', 'y', 'len', 'mag']

    def __init__(self, x=0, y=0):
        self.x = x; self.y = y

        self.len = math.sqrt(self.x**2+self.y**2)
        self.mag = self.len
  


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__getattribute__(self.__slots__[item])
            #return self.lis[item]
        if isinstance(item, str):
            return self.__getattribute__(item)
            #return self.lib[item]


    def __setitem__(self, item, insert):
        if isinstance(item, int):
            self.__setattr__(self.__slots__[item], insert)
            #self.lis.__setitem__(item, insert) #?
            #self.lis[item] = insert            #?
        if isinstance(item, str):
            self.__setattr__(item, insert)

    def length(self):
        self.len = math.sqrt(self.x**2+self.y**2)
        return self.len


    def __add__(self, other):
        newx = self.x + other.x; newy = self.y + other.y
        return Vec(newx, newy)

    def __sub__(self, other):
        newx = self.x - other.x; newy = self.y - other.y
        return Vec(newx, newy)

    def __mul__(self, scale : (float or int)):
        newx = self.x * scale; newy = self.y * scale
        self.x *= scale; self.y *= scale
        return Vec(newx, newy)


    def __str__(self):
        return f'({round(self.x)},{round(self.y)})'


    def setList(self, x, y):
        self.lis = [x,y]

    def asTuple(self):
        return (self.x,self.y)

    def __round__(self):
        self.x, self.y = round(self.x), round(self.y)

    def printExact(self):
        print(f'({self.x},{self.y})')

    def copy(self):
        return Vec(copy.copy(self.x),copy.copy(self.y))


