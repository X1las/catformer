import math
import copy



# (A part of) the Vec class:
class Vec():
    def __init__(self, x, y):
        self.x = x; self.y = y;
    
       
        self.len = math.sqrt(self.x**2+self.y**2)
        self.mag = self.len
        self.lis = [self.x,self.y]
        self.lib  = {'x' : self.x, 'y': self.y}
        

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.lis[item]
        if isinstance(item, str):
            return self.lib[item]

    def __setitem__(self, item, insert):
        if isinstance(item, int):
            self.lis.__setitem__(item, insert) #?
            self.lis[item] = insert            #?
        if isinstance(item, str):
            return self.lib.__setitem__(item, insert)

    def asTuples(self):
        return (self.x, self.y)


    def __add__(self, other):
        newx = self.x + other.x; newy = self.y + other.y
        return Vec(newx, newy)

    def __sub__(self, other):
        newx = self.x - other.x; newy = self.y - other.y
        return Vec(newx, newy)

    def __mult__(self, scale : (float or int)):
        newx = self.x * scale; newy = self.y * scale
        return Vec(newx, newy)


    def __str__(self):
        return f'({round(self.x)},{round(self.y)})'


    def __round__(self):
        self.x, self.y = round(self.x), round(self.y)

    def printExact(self):
        print(f'({self.x},{self.y})')

    def copy(self):
        return Vec(copy.copy(self.x),copy.copy(self.y))

