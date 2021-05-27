# Description:

# Imports
import math, copy

# Classes
class Vec(object):

    # Class Variables
    __slots__=['x', 'y', 'len', 'mag']


    def __init__(self, x=0, y=0):
        self.x = x; self.y = y


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
        #self.x *= scale; self.y *= scale
        return Vec(newx, newy)


    def __truediv__(self, scale : (float or int)):
        newx = self.x / scale; newy = self.y / scale
        #self.x *= scale; self.y *= scale
        return Vec(newx, newy)


    def __str__(self):
        return f'({self.x},{self.y})'


    def __abs__(self):
        newx = abs(self.x)
        newy = abs(self.y)
        return Vec(newx, newy)


    def setList(self, x, y):
        self.lis = [x,y]


    def asTuple(self):
        return (self.x,self.y)


    def __round__(self):
        self.x, self.y = round(self.x), round(self.y)


    def rounded(self):
        #return self.realRound()
        roundedx = self.normRound(self.x)
        roundedy = self.normRound(self.y)
        return Vec(roundedx,roundedy)


    def realRound(self):
        #return self.rounded()
        roundedx = self.rounding(self.x)
        roundedy = self.rounding(self.y)
        return Vec(roundedx,roundedy)    

        
    def roundUp(self):
        roundedx = self.roundUpN(self.x)
        roundedy = self.roundUpN(self.y)
        return Vec(roundedx,roundedy)    


    def normRound(self, number):
        inte = math.floor(number)
        dec = number - inte
        if dec*10 >= 5:
            result = 1
        else:
            result = 0
        return inte + result


    def roundUpN(self, number):
        rounded_num = number
        rounded_num = math.floor(rounded_num)
        return rounded_num        


    def similarTo(self, other, deltaX, deltaY):
        return abs(self.x - other.x) <= deltaX and abs(self.y - other.y) <= deltaY 


    def rounding(self, number):
        neg = False
        if number < 0:
            neg = True
        rounded_num = number
        rounded_num = math.ceil(abs(rounded_num))
        if neg:
            rounded_num *= -1
        return rounded_num        


    def printExact(self):
        print(f'({self.x},{self.y})')


    def copy(self):
        return Vec(copy.copy(self.x),copy.copy(self.y))


