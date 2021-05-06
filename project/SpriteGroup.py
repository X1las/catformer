import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class SpriteGroup(pg.sprite.LayeredUpdates):

    def update(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.update_order, reverse = False)
        for i in lis:
            i.update()

    def updatePos(self, solid):
        for i in self:
            i.updatePos(solid)
            i.posCorrection()
        #self.correctPositions()

    def correctPositions(self):
        for i in self:
            i.posCorrection()
    
    def getObject(self, name):
        for i in self:
            if i.name == name:
                return i



