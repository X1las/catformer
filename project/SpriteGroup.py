import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class SpriteGroup(pg.sprite.LayeredUpdates):

    def updateOrder(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.update_order, reverse = False)
        return lis

    def update(self):
        lis = self.updateOrder()
        for i in lis:
            i.update()

    def updatePos(self, solid):
        lis = self.updateOrder()
        for i in lis:
            i.updatePos(solid)
            #i.posCorrection()
        """ So, if box is pushing into something and getting pushed out, player is already updated before the box was pushed out, so it vibrates"""
        self.correctPositions()
        #self.correctPositions()

    def correctPositions(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.solidstrength, reverse = True)
        for i in lis:
            i.posCorrection()
    
    def getObject(self, name):
        for i in self:
            if i.name == name:
                return i



