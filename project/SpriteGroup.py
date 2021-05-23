import pygame as pg
from Vector import *
from settings import *
import math

vec = Vec


class SpriteGroup(pg.sprite.LayeredUpdates):
    orderedList = None
    massOrdered = None

    def __init__(self):
        pg.sprite.LayeredUpdates.__init__(self)

    def resetRects(self):
        for i in self:
            i.resetRects()

    def updateRects(self):
        for i in self:
            i.updateRect()

    def resetSprites(self):
        for i in self:
            i.resetSprite()

    def updateOrder(self):
        if not self.orderedList:
            self.orderedList = self.createOrderedList()
        #self.orderedList.sort(key = lambda x: x.update_order, reverse = False)
        return self.orderedList

    def createOrderedList(self):
        self.orderedList = self.sortList()
        return self.orderedList

    def collisionEffects(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.solidstrength, reverse = True)
        for i in lis:
            i.pushEffect()
        
    def massUpdateOrder(self):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        return self.massOrdered


    def massSort(self, key):
        if not self.massOrdered:
            self.massOrdered = self.createMassOrdered()
        elif key == "massHOR":
            self.massOrdered.sort(key = lambda x: x.massHOR, reverse = True)
        elif key == "massVER":
            self.massOrdered.sort(key = lambda x: x.massVER, reverse = True)
        return self.massOrdered

    def createMassOrdered(self):
        lis = []

        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.solidstrength, reverse = False)
        return lis


    def sortList(self):
        lis = []
        for i in self:
            lis.append(i)
        lis.sort(key = lambda x: x.update_order, reverse = False)
        return lis

    def update(self):
        lis = self.updateOrder()
        for i in lis:
            i.update()

    def update2(self):
        lis = self.updateOrder()
        for i in lis:
            i.update2()


    def updateAddedvel(self):
        lis = self.updateOrder()

        for i in lis:
            i.updateAddedVel()


    def updatePos(self):
        lis = self.updateOrder()
        for i in lis:
            i.updatePos()
            #i.posCorrection()
        """ So, if box is pushing into something and getting pushed out, player is already updated before the box was pushed out, so it vibrates"""
        self.correctPositions()

    def correctPositions(self):
        self.massSort('massVER')
        for i in self.massOrdered:
            i.posCorrection()
        self.massSort("massHOR")
        for i in self.massOrdered:
            i.posCorrection()
        


